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

class Bambu(BasecampFlowModule):

    def compile(self, **kwargs):
        print("This feature is currently not supported for the synthesis flow.")
        raise NotImplementedError

    def cli(self, args, config):
        try:
            subprocess.run(["which", "bambu"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            print("Bambu is not installed or not on PATH.")
            return
    
        command = ["bambu", "--compiler=I386_CLANG12", "--generate-interface=INFER",
           f"--top-fname={args['--top-fname']}", args['<input-file>']]

        # Add all remaining elements of args to the command
        for key, value in args.items():
            if key in ['--device-name', '--clock-period']:
                if value is not None:
                    command.append(f"{key}={value}")

        # Run the subprocess command
        subprocess.run(command)
        
        return 0
