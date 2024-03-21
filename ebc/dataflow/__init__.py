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

from .ohua import Ohua

module = Ohua
identifier = 'dataflow'

docstrs = {'usage': 'dataflow (--dfg-src <input-file>|--olympus-src <input-file>) [--dfg-out <path-to-output>] [--olympus-out <path-to-output>] [--architecture <arch.json>] [--target <target>] [--threads <num>] '
                    '[--enable-parallelism <bool>] [--c-limit <num>] [--amorphous <bool>]',
           'commands': ('dataflow', 'Invokes the dataflow flow of the EVEREST SDK.'),
           'options': [
               ('--dfg-out <path-to-output>', 'Path to save generated dfg files under (defualts to `generated`).'),
               ('--olympus-out <path-to-output>', 'Path to save generated Olympus files under (defualts to `olympus_gen`).'),
               ('--architecture <arch.json>', 'Architecture description for Olympus in JSON format.'),
               ('--target <target>', 'Target for the code generator (supported values: rust, mlir).'),
               ('--threads <num>', 'Number of threads to parallelize for (default: number of local cores).'),
               ('--enable-parallelism <bool>', 'Whether to enable the parallelization optimization (defaults to `true`).'),
               ('--c-limit <num>', 'Number of maximum collisions for a computation with amorphous data parallelism.'),
               ('--amorphous <bool>', 'Whether to enable the transformation of amorphous data parallel tasks (defaults to `false`).'),
            ]}
