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
import logging


class BasecampFlowModule(metaclass=abc.ABCMeta):

    def __init__(self, identifier):
        self.flow_identifier = identifier
        self.log = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def compile(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def cli(self, args, config):
        raise NotImplementedError

