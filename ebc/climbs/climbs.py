import sys
import os
import json
import subprocess

from ebc.flow_module import BasecampFlowModule

__filedir__ = os.path.dirname(os.path.abspath(__file__))
# __supported_languages__ = ['python', 'cpp', 'docker']
__supported_languages__ = ['python', 'docker']


class Climbs(BasecampFlowModule):

    def __init__(self):
        super().__init__()
        # self._initialized_machine_specific = False
        self.description_paths = {}
        self.flow_language_wrappers_init = {}
        for sl in __supported_languages__:
            self.flow_language_wrappers_init[sl] = {}
        self.flow_language_wrappers_run = {}
        for sl in __supported_languages__:
            self.flow_language_wrappers_run[sl] = {}
        self.flow_language_wrappers_check = {}
        for sl in __supported_languages__:
            self.flow_language_wrappers_check[sl] = {}

    def add_flow_module(self, identifier, mod, flow_obj: BasecampFlowModule):
        climbing_dict = mod.climbing
        self.description_paths[identifier] = os.path.abspath(os.path.join(
            __filedir__, '../', climbing_dict['description_path']))
        for lang, path in climbing_dict['init'].items():
            if lang not in __supported_languages__:
                self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
                continue
            self.flow_language_wrappers_init[lang][identifier] = os.path.abspath(os.path.join(
                __filedir__, '../', path))
        for lang, path in climbing_dict['run'].items():
            if lang not in __supported_languages__:
                self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
                continue
            self.flow_language_wrappers_run[lang][identifier] = os.path.abspath(os.path.join(
                __filedir__, '../', path))
        for lang, path in climbing_dict['runtime_check'].items():
            if lang not in __supported_languages__:
                self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
                continue
            self.flow_language_wrappers_check[lang][identifier] = os.path.abspath(os.path.join(
                __filedir__, '../', path))

    def climbing(self, climb_dict):
        return None

    def compile(self, **kwargs):
        self.climbing(**kwargs)

    def cli(self, args, config):
        if args['describe'] is not None:
            self.describe(args['--flow'])

    def describe(self, flow_req):
        if flow_req not in self.description_paths:
            self.log.error("No description for this flow available.")
        else:
            os.system(f"cat {self.description_paths[flow_req]}")

