
import sys
import os

__filedir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, __filedir__)
import dataflow
import hpc
import ml
import automatic


class EverestBasecamp:

    def __init__(self, load_modules='default'):
        if load_modules == 'default':
            load_modules = [dataflow, hpc, ml, automatic]
        self._flows = {}
        self._doc_dict = {}
        self.docstr = "EVEREST basecamp -- The basis for all EVEREST endeavors.\n\n"
        for mod in load_modules:
            self._flows[mod.identifier] = mod.module()
            setattr(self, mod.identifier, self._flows[mod.identifier])
            self._doc_dict[mod.identifier] = mod.docstrs


