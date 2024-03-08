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

from .cfdlang import Cfdlang

module = Cfdlang
identifier = 'hpc'

docstrs = {'usage': 'hpc [--lang <lang-id> --pipeline <pipeline> (-D <define>...) (-I <include>...)] <input> -o <path-to-output>',
           'commands': ('hpc', 'Invokes the HPC flow of the EVEREST SDK.'),
           'options': []}
