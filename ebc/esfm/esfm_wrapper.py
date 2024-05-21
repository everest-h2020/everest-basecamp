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
    esfm_cli = ""
    list_vfs = ""
    list_vf_vm = ""
    print_kernel = ""
    attach = ""
    detach = ""
    init = ""
    bitstream = ""
    if args["<pf_dev>"] != "" and args["esfm"] == True:
      if args["list_vfs"]:
        list_vfs = "list_vfs"
      if args["print_kernel"]:
        list_vfs = "print_kernel"
      if args["list_vf_vm"]:
        list_vf_vm = "list_vf_vm"
      if args["attach"]:
        if args["<vf_idx>"] and args["<vm_name>"]:
          attach = str("attach " + args["<vf_idx>"]) + " " + args["<vm_name>"]
      if args["detach"]:
        if args["<vf_idx>"]:
          detach = "detach " + str(args["<vf_idx>"])
      if args["init"] and args["<vf_num>"]:
        init = "init " + str(args["<vf_num>"])
        if not((args["--bitstream"] != None) ^ (args["<kernel_type>"] != None)):
          bitstream = "--bitstream " + args["<path_to_bitstream>"] + " " + args["<kernel_type>"]
        elif args["--bitstream"] or args["<kernel_type>"] == None:
          raise ValueError("Incorrect parameters: bitstream and kernel type option must be used together")
    else:
      raise ValueError("Incorrect parameters")
    esfm_cli = "esfm" + " " + args["<pf_dev>"] + " " + list_vfs + print_kernel + list_vf_vm + attach + detach + init + " " +bitstream
    res = subprocess.call(__filedir__ + "/" + esfm_cli,shell=True)

  def compile(self, **kwargs):
    self.log.error("Esfm is a bash script")
    raise NotImplementedError
