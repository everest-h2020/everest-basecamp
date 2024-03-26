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
import json
import subprocess

from pathlib import Path
from ebc.flow_module import BasecampFlowModule

__filedir__ = os.path.dirname(os.path.abspath(__file__))

class EsfmWrapper(BasecampFlowModule):
  def __init__(self, identifier):
    super().__init__(identifier)

  def cli(self, args, config):
    if args['<pf_dev>'] and args['esfm'] :
      #build input for esfm
      esfm_cli = ""
      # Cycle through every true optoion
      for opt in args:
        if args[opt]:
          if isinstance(args[opt],bool):
            esfm_cli = esfm_cli + opt + " "
          else:
            esfm_cli = esfm_cli + str(args[opt]) + " "

      res = subprocess.call(__filedir__ + "/" + esfm_cli,shell=True)

  def compile(self, **kwargs):
    self.log.error("Esfm is a bash script")
    raise NotImplementedError
