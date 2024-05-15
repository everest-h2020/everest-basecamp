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

from .messner import Messner

module = Messner
identifier = 'hpc'

docstrs = {'usage': 'hpc [--ekl-passes <pipeline>] [--messner-out <path-to-output>] '
                    '<input-file> '
                    '[--mlir-disable-threading] [--mlir-print-ir-after-failure] '
                    '[--mlir-print-debuginfo] [--mlir-print-op-generic]',
           'commands': ('hpc', 'Invokes the messner compiler for the EVEREST kernel language (EKL).'),
           'options': [
                ('--ekl-passes <pipeline>',        'Textual MLIR pass pipeline to augment default pipeline.'),
                ('--messner-out <path-to-output>', 'Path to the messner MLIR output directory (defaults to `generated`).'),
                ('--mlir-disable-threading',       'Disable multithreading during MLIR optimization passes.'),
                ('--mlir-print-ir-after-failure',  'Print the MLIR to stderr when compilation fails.'),
                ('--mlir-print-debuginfo',         'Emit debug information and source locations in the MLIR output.'),
                ('--mlir-print-op-generic',        'Emit generic MLIR for non-EVEREST SDK tools.'),
           ]}
