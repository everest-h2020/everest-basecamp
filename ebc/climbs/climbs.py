import os

from ebc.flow_module import BasecampFlowModule

__filedir__ = os.path.dirname(os.path.abspath(__file__))
# __supported_languages__ = ['python', 'cpp', 'docker']
__supported_languages__ = ['python', 'docker']

__climb_api_version__ = 0.1

__climb_file_template__ = {'name': '', 'climb_version': __climb_api_version__,
                           'out_path': '',
                           'main_files': [],  # list of tuples: (path, language)
                           'variants': [],  # list of path to module.section
                           }

__section_file_template__ = {'module': '', 'climb_version': __climb_api_version__,
                             'init_format_dict': {},
                             'run_format_dict': {},
                             'files_dirs_to_copy': [],
                             }
__from_pragma_string__ = 'BASECAMP_CLIMBS_PRAGMA_DEF'


class Climbs(BasecampFlowModule):

    def __init__(self):
        super().__init__()
        # self._initialized_machine_specific = False
        self.description_paths = {}
        self.flow_language_wrappers_init = {}
        # for sl in __supported_languages__:
        #     self.flow_language_wrappers_init[sl] = {}
        # self.flow_language_wrappers_run = {}
        # for sl in __supported_languages__:
        #     self.flow_language_wrappers_run[sl] = {}
        self.flow_language_wrappers_check = {}
        for sl in __supported_languages__:
            self.flow_language_wrappers_check[sl] = {}

    def add_flow_module(self, identifier, mod, flow_obj: BasecampFlowModule):
        from ebc.climb_module import BasecampClimbModule
        if not isinstance(flow_obj, BasecampClimbModule):
            self.log.error(f"Module {identifier} does not support the creation of climbs (yet). STOP")
            exit(-1)
        climbing_dict = mod.climbing
        self.description_paths[identifier] = os.path.abspath(os.path.join(
            __filedir__, '../', climbing_dict['description_path']))
        # for lang, path in climbing_dict['init'].items():
        #     if lang not in __supported_languages__:
        #         self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
        #         continue
        #     self.flow_language_wrappers_init[lang][identifier] = os.path.abspath(os.path.join(
        #         __filedir__, '../', path))
        # for lang, path in climbing_dict['run'].items():
        #     if lang not in __supported_languages__:
        #         self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
        #         continue
        #     self.flow_language_wrappers_run[lang][identifier] = os.path.abspath(os.path.join(
        #         __filedir__, '../', path))
        for lang, check_tuple in climbing_dict['runtime_check'].items():
            if lang not in __supported_languages__:
                self.log.warning(f'language {lang} of module {identifier} not supported, skipping.')
                continue
            self.flow_language_wrappers_check[lang][identifier] = (os.path.abspath(os.path.join(
                __filedir__, '../', check_tuple[0])), check_tuple[1])
        flow_obj.set_climb_obj(self)

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

    def create_module_section(self, init_format_dict, run_format_dict, files_dirs_to_copy, out_path):
        return None
