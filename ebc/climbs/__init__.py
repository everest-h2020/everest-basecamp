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

from .climbs import Climbs, __supported_languages__

module = Climbs
identifier = 'climbs'

docstrs = {'usage': 'climbs (describe --flow <flow> | '
                    'create --name <name> <path-to-file.climb> | '
                    'add_module --module <path-to-module.section> <path-to-file.climb> | '
                    'add_file --file <path-to-source.file> --language <language> <path-to-file.climb> | '
                    'emit <path-to-file.climb> [--output-directory <path-to-output-directory>])',
           'commands': ('climbs', 'Combines different flows (i.e. "everest climbs") to one application.'),
           'options': [
               ('describe', 'Describes the required API for the flow.'),
               ('--flow <flow>', 'Specifies the flow to describe.'),
               ('create', 'Create a new flow.'),
               ('add_module --module', 'Add a new application variant to an existing climb.'),
               ('add_file --file', 'Add file (with annotations) of the main application to the climb.'),
               ('--language <language>', f'The langauge of the added file. Currently supported are: '
                                         f'{", ".join(__supported_languages__)}. '
                                         f'(Copy means the file will be copied without change.)'),
               ('emit', 'Emit created climb to build directory.')
           ]}
