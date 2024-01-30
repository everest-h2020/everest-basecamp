import sys
import os
import json
from pathlib import Path

from ebc.flow_module import BasecampFlowModule
# from ebc.climb_module import BasecampClimbModule
# from ebc.climbs.climbs import Climbs, __from_pragma_string__

__filedir__ = os.path.dirname(os.path.abspath(__file__))


class AirflowWrapper(BasecampFlowModule):
    def __init__(self, identifier):
        super().__init__(identifier)
        self._initialized_machine_specific = False

    def cli(self, args, config):
        pass

    def compile(self, **kwargs):
        pass

