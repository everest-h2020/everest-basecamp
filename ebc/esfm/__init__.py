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

from .esfm_wrapper import EsfmWrapper

module = EsfmWrapper
identifier = 'esfm'

docstrs = {'usage': f'{identifier} <pf_dev> ( init | reconf | attach | detach | list_vfs | list_vf_vm | print_kernel )',
           'commands': (f'{identifier}', 'User interface to handle virtualization framework'),
           'options': [
               ('init <VF_NUM>',             'Init PF device with VF_NUM virtual functions'),
               ('reconf <VF_NUM>',           'Reconfigure num of VF'),
               ('attach <VF_IDX> <VM_NAME>', 'Attach VF_IDX to VM_NAME'),
               ('detach <VF_IDX>',           'Detach VF_IDX from the VM it is attached to'),
               ('list_vfs',                  'List VF for a given PF'),
               ('list_vf_vm',                'List VF association to VM'),
               ('print_kernel',              'Print latest kernel flashed inside <pf_dev>'),
           ]}
