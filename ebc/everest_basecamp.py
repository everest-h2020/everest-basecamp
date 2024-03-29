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

import sys
import os

__filedir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, __filedir__)
import climbs

# import individual modules below
# --------------------------------
import dataflow
import hpc
import ml
import airflow
import synthesis
# --------------------------------


__cli_name__ = 'ebc-cli'
__softtab__ = '    '
__docstr_column_width = 50


def _make_docstr_line(tab, c1, c2):
    ret = tab + c1
    scnt = max(__docstr_column_width - len(c1), 0)
    ret += ' ' * scnt
    ret += c2
    ret += '\n'
    return ret


class EverestBasecamp:

    def __init__(self, load_modules='default'):
        if load_modules == 'default':
            # list modules to load below
            # --------------------------------
            load_modules = [dataflow, hpc, ml, climbs, airflow, synthesis]
            # --------------------------------
        self._flows = {}
        self._doc_dict = {}
        for mod in load_modules:
            self._flows[mod.identifier] = mod.module(mod.identifier)
            setattr(self, mod.identifier, self._flows[mod.identifier])
            self._doc_dict[mod.identifier] = mod.docstrs
        # TODO: init climb flows hasattr(mod, 'climb')
        for mod in load_modules:
            if hasattr(mod, 'climbing'):
                self._flows[climbs.identifier].add_flow_module(mod.identifier, mod, self._flows[mod.identifier])
        self._cli_dict = {}
        self.docstr = ''
        self._build_docstr()

    def _build_docstr(self):
        docstr = "EVEREST basecamp -- the basis for all EVEREST endeavors.\n\n"
        docstr += "Usage:\n"
        for mod in self._doc_dict:
            mod_usage = self._doc_dict[mod]['usage']
            docstr += f'{__softtab__}{__cli_name__} {mod_usage}\n'
        docstr += f'{__softtab__}{__cli_name__} -h|--help\n'
        docstr += f'{__softtab__}{__cli_name__} -v|--version\n'
        docstr += '\nCommands:\n'
        for mod in self._doc_dict:
            command_tuple = self._doc_dict[mod]['commands']
            docstr += _make_docstr_line(__softtab__, command_tuple[0], command_tuple[1])
            self._cli_dict[command_tuple[0]] = self._flows[mod].cli
        docstr += '\nOptions:\n'
        docstr += _make_docstr_line(__softtab__, '-h --help', 'Show this screen.')
        docstr += _make_docstr_line(__softtab__, '-v --version', 'Show version.')
        docstr += '\n'
        for mod in self._doc_dict:
            for optpl in self._doc_dict[mod]['options']:
                docstr += _make_docstr_line(__softtab__, optpl[0], optpl[1])
        docstr += '\n'
        docstr += 'Copyright EVEREST Consortium, licensed under the Apache License 2.0.\n' \
                  'For contact and more details please visit: https://everest-h2020.eu\n'
        self.docstr = docstr

    def cli(self, arguments):
        for command, clicall in self._cli_dict.items():
            if arguments[command]:
                # TODO: do we need the config?
                return clicall(arguments, None)
        # actually, docopt checks the correctness before...so there should be a clicall in all cases
