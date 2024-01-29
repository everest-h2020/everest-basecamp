
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
