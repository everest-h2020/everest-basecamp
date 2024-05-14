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

from subprocess import run
from shutil import which
from pathlib import Path

class Messner(BasecampFlowModule):

    def compile(self, **kwargs):
        print("This feature is currently not supported for the messner flow.")
        raise NotImplementedError

    def cli(self, args, config):
        messner = which('messner')
        if messner is None:
            print("Could not find messner executable.")
            return

        input_file = Path(args['<input-file>'])
        if not input_file.exists():
            print("Input file does not exist.")
            return

        command = [messner, input_file]

        # Ensure the output directory exists and make the output file name.
        out_dir = Path(args.get('--messner-out') or './generated')
        out_dir.mkdir(parents=True, exist_ok=True)
        out_name = input_file.with_suffix('.kernels.mlir')
        command.append('-o')
        command.append(f'{out_dir.joinpath(out_name)}')

        # Serialize the pass pipeline.
        pass_pipeline = args.get('--ekl-passes') or ''
        command.append(f'--pass-pipeline="{pass_pipeline}"')

        # Forward miscellaneous MLIR options.
        for key, value in args.items():
            if key.startswith('--mlir-'):
                if value is True:
                    command.append(f'{key}')
                elif value is False or value is None:
                    pass
                else:
                    command.append(f'{key}="{value}"')

        # Delegate to the messner CLI facade.
        return run(command).returncode

