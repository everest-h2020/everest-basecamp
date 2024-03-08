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
import logging

from .everest_basecamp import EverestBasecamp

if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
    # This works with virtualenv for Python 3 and 2 and also for the venv module in Python 3
    print("[ebc:ERROR] It looks like this basecamp isn't running in a virtual environment. STOP.")
    sys.exit(1)

FORMAT = '%(levelname)-9s %(threadName)-15s %(name)-15s: %(funcName)-15s %(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level='WARNING')

basecamp = EverestBasecamp()
