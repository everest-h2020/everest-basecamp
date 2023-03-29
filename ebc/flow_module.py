
import abc


class BasecampFlowModule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def compile(self, args):
        print("ABSTRACT METHOD")
        return -1

