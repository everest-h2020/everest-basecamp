
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

