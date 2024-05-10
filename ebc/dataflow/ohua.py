#  /*******************************************************************************
#   * Copyright 2022 -- 2024 EVEREST consortium (everest-h2020.eu)
#   *
#   * Licensed under the Apache License, Version 2.0 (the "License");
#   * you may not use this file except in compliance with the License.
#   * You may obtain a copy of the License at
#   *
#   *     http://www.apache.org/licenses/LICENSE-2.0
#   *
#   * Unless required by applicable law or agreed to in writing, software
#   * distributed under the License is distributed on an "AS IS" BASIS,
#   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   * See the License for the specific language governing permissions and
#   * limitations under the License.
#  *******************************************************************************/
#

from ebc.flow_module import BasecampFlowModule

import datetime
import os
import subprocess
import sys
import yaml


OHUA_CONFIG = {
    "extra-features": ["tail-recursion"],
    "integration-features": {
        "arch": "SharedMemory",
        "options": {}
    },
    "debug": { "log-level": "info" }
}

# NOTE(feliix42): generate programmatically from the filename?
__lowered_mlir__ = "lowered.mlir"
__olympus_mlir__ = "olympus.mlir"
__lowered_ll_ = "lowered.ll"

class Ohua(BasecampFlowModule):

    def compile(self, **kwargs):
        print("This feature is not supported for dataflow flows")
        raise NotImplementedError

    def cli(self, args, config):
        global OHUA_CONFIG
        # TODO:
        # - config file for dfg path
        # - config for ohua path?

        # paths
        dfg_outdir = args["--dfg-out"] if args["--dfg-out"] is not None else "generated"
        ohua_outdir = args["--ohua-out"] if args["--ohua-out"] is not None else "generated"
        olympus_outdir = args["--olympus-out"] if args["--olympus-out"] is not None else "generated"
        olympus_mlir = args["<input-file>"] if args["--olympus-src"] else __olympus_mlir__

        # if ohua -> rust-to-rust, ignore the rest
        # if dfg -> dfg -> (olympus if platform file)
        # if oly -> (olympus if platform file)

        if args["--ohua-src"]:
            print(args)
            target = args["--target"] if args["--target"] is not None else "rust"
            if target != "rust":
                print("ERROR: Unsupported target.")
                sys.exit(1)

            if args["--enable-parallelism"] == True or args["--enable-parallelism"] is None:
                num_threads = int(args["--threads"]) if args["--threads"] is not None else os.cpu_count()
                OHUA_CONFIG["integration-features"]["options"]["data-parallelism"] = num_threads

            if args["--amorphous"]:
                if args["--c-limit"] is None:
                    print("ERROR: must specify the --c-limit <num> value")
                    sys.exit(1)

                limit = int(args["--c-limit"])
                OHUA_CONFIG["integration-features"]["options"]["amorphous"] = limit

            config_file = "/tmp/ohua-config-{}.yaml".format(datetime.datetime.now().isoformat())
            with open(config_file, 'w') as ohua_cnf:
                yaml.dump(OHUA_CONFIG, ohua_cnf)

            res = subprocess.run(["mkdir", "-p", ohua_outdir])
            # TODO: check if res == ok
            res = subprocess.run(["rm", "-rf", "{}/*".format(ohua_outdir)])
            # TODO: check if res == ok

            modname = os.path.basename(args['<input-file>']).split('.')[0]
            print(modname)
            with open("{}/lib.rs".format(ohua_outdir), 'w') as f:
                f.write("pub mod {};".format(modname))
                # TODO: Multiple files? Append mode?

            res = subprocess.run(["ohuac", "build", args['<input-file>'], "-o", ohua_outdir, "-c", config_file])
            # TODO: check if res == ok

        elif args["--dfg-src"]:
            with open(dfg_outdir + '/' + __lowered_mlir__, 'w') as f:
                res = subprocess.run([
                    "dfg-opt", "--insert-olympus-wrappers", "--convert-dfg-nodes-to-func", "--convert-scf-to-cf",
                    "--convert-cf-to-llvm", "--convert-dfg-edges-to-llvm", "--convert-arith-to-llvm",
                    "--convert-func-to-llvm", "--canonicalize", args['<input-file>']
                ], stdout=f)
                # TODO: Check if res == ok

            with open(dfg_outdir + '/' + __olympus_mlir__, 'w') as f:
                res = subprocess.run([
                    "dfg-opt", "--convert-dfg-to-olympus", "--allow-unregistered-dialect", "-mlir-print-op-generic", args['<input-file>']
                ], stdout=f)
                # TODO: Check if res == ok

            with open(dfg_outdir + '/' + __lowered_ll__, 'w') as f:
                res = subprocess.run([
                    "mlir-translate", "--mlir-to-llvmir", args['-o'] + __lowered_mlir__
                ], stdout=f)
                # TODO: Check if res == ok

            if args["--architecture"] is not None:
                # run olympus
                res = subprocess.run([
                    "olympus", "--platform", args["--architecture"], "--application",
                    olympus_mlir, "--output", olympus_outdir
                ])
        else:
            if args["--architecture"] is None:
                print("--architecture <arch.json> needs to be specified")
                return 1

            # run olympus
            res = subprocess.run([
                "olympus", "--platform", args["--architecture"], "--application",
                olympus_mlir, "--output", olympus_outdir
            ])

        return 0


