
from ebc.flow_module import BasecampFlowModule


class Cfdlang(BasecampFlowModule):

    def compile(self, **kwargs):
        print("Please ask Karl for the state of this flow...")
        raise NotImplementedError

    def cli(self, args, config):
        print("Please ask Karl for the state of this flow...")
        raise NotImplementedError
