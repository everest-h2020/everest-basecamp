
from ebc.flow_module import BasecampFlowModule


class Ohua(BasecampFlowModule):

    def compile(self, **kwargs):
        print("Please ask Felix for the state of this flow...")
        raise NotImplementedError

    def cli(self, args, config):
        print("Please ask Felix for the state of this flow...")
        raise NotImplementedError

