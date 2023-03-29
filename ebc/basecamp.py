
import dataflow
import hpc
import ml
import automatic


class EverestBasecamp(object):

    def __int__(self, load_modules='default'):
        if load_modules is 'default':
            load_modules = [dataflow, hpc, ml, automatic]
        self.flows = {}
        for mod in load_modules:
            self.flows[mod.identifier] = mod.module()
            setattr(self, mod.identifier, self.flows[mod.identifier])


