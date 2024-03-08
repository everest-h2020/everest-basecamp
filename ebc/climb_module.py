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

import abc


class BasecampClimbModule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_run_code(self, args, language):
        raise NotImplementedError

    @abc.abstractmethod
    def get_init_code(self, args, language):
        raise NotImplementedError

    @abc.abstractmethod
    def set_climb_obj(self, climb_obj):
        raise NotImplementedError

    @abc.abstractmethod
    def get_install_notes(self):
        raise NotImplementedError
