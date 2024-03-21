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

import subprocess

# NOTE(feliix42): generate programmatically from the filename?
__lowered_mlir__ = "lowered.mlir"
__olympus_mlir__ = "olympus.mlir"
__lowered_ll_ = "lowered.ll"

class Ohua(BasecampFlowModule):

    def compile(self, **kwargs):
        print("This feature is not supported for dataflow flows")
        raise NotImplementedError

    def cli(self, args, config):
        # TODO:
        # - config file for dfg path
        # run dfg (llvm, olympus, llvmirjj)
        print(args)

        # paths
        dfg_outdir = args["--dfg-out"] if args["--dfg-out"] is not None else "generated"
        olympus_outdir = args["--olympus-out"] if args["--olympus-out"] is not None else "generated"
        olympus_mlir = args["<input-file>"] if args["--olympus-src"] else __olympus_mlir__

        # if dfg -> dfg -> (olympus if platform file)
        # if oly -> (olympus if platform file)

        if args["--dfg-src"]:
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


