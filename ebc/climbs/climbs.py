import json
import os
from pathlib import Path

from ebc.flow_module import BasecampFlowModule

__filedir__ = os.path.dirname(os.path.abspath(__file__))
# __supported_languages__ = ['python', 'cpp', 'docker']
__supported_programming_languages__ = ['python', 'docker']
__supported_languages__ = __supported_programming_languages__ + ['copy']

__climb_api_version__ = 0.1

__climb_file_template__ = {'name': '', 'climb_version': __climb_api_version__,
                           'out_dir': '',
                           'main_files': [],  # list of tuples: (path, language)
                           'variants': [],  # list of path to module.section
                           }

__section_file_template__ = {'module': '', 'climb_version': __climb_api_version__,
                             'init_format_dict': {},
                             'run_format_dict': {},
                             'relative_files_dirs_to_copy': [],
                             }
__from_pragma_string__ = 'BASECAMP_CLIMBS_PRAGMA_DEF'


def get_comment_string(lang):
    __ebc_comment__ = 'generated by EVEREST basecamp'
    assert lang in __supported_programming_languages__
    # '#' as comment
    if lang in ['python', 'docker']:
        return f'# {__ebc_comment__}'


def _harmonizing_climb_file_path(climb_file_path):
    if climb_file_path[-6:] != '.climb':
        climb_file_path += '.climb'
    return os.path.abspath(climb_file_path)


class Climbs(BasecampFlowModule):

    def __init__(self, identifier):
        super().__init__(identifier)
        # self._initialized_machine_specific = False
        self.description_paths = {}
        self.flow_language_wrappers_init = {}
        # for sl in __supported_languages__:
        #     self.flow_language_wrappers_init[sl] = {}
        # self.flow_language_wrappers_run = {}
        # for sl in __supported_languages__:
        #     self.flow_language_wrappers_run[sl] = {}
        self.flow_language_wrappers_check = {}
        for sl in __supported_programming_languages__:
            self.flow_language_wrappers_check[sl] = {}
        self.flow_obj_dict = {}

    def add_flow_module(self, identifier, mod, flow_obj: BasecampFlowModule):
        from ebc.climb_module import BasecampClimbModule
        if not isinstance(flow_obj, BasecampClimbModule):
            self.log.error(f"Module {identifier} does not support the creation of climbs (yet). STOP")
            exit(-1)
        self.flow_obj_dict[identifier] = flow_obj
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
            if lang not in __supported_programming_languages__:
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
        # print(args)
        if args['describe']:
            self.describe(args['--flow'])
        if args['create']:
            self.create(args['<name>'], args['<path-to-file.climb>'])
        if args['add_module']:
            self.add_module(args['<path-to-module.section>'], args['<path-to-file.climb>'])
        if args['add_file']:
            self.add_file(args['<path-to-source.file>'], args['--language'], args['<path-to-file.climb>'])
        if args['emit']:
            self.emit(args['<path-to-file.climb>'], args['<path-to-output-directory>'])

    def describe(self, flow_req):
        if flow_req not in self.description_paths:
            self.log.error("No description for this flow available.")
        else:
            os.system(f"cat {self.description_paths[flow_req]}")

    def create(self, name, climb_file_path):
        climb_file = __climb_file_template__.copy()
        climb_file['name'] = name
        if climb_file_path[-1] == '/':
            if not os.path.isdir(climb_file_path):
                os.system(f"mkdir -p {climb_file_path}")
        if os.path.isdir(climb_file_path) and not os.path.isfile(climb_file_path):
            climb_file_path += f'/{name}.climb'
        climb_file_path = _harmonizing_climb_file_path(climb_file_path)
        climb_file['out_dir'] = os.path.dirname(climb_file_path)
        with open(climb_file_path, 'w') as f:
            json.dump(climb_file, f)
        # self.log.info(f"Climb {climb_file_path} created successfully.")
        print(f"Climb {climb_file_path} created successfully.")

    def add_module(self, module_section_file_path, climb_file_path):
        climb_file_path = _harmonizing_climb_file_path(climb_file_path)
        with open(climb_file_path, 'r') as f:
            climb_file = json.load(f)
        if module_section_file_path[-8:] != '.section':
            module_section_file_path += '.section'
        module_section_file_path = os.path.abspath(module_section_file_path)
        with open(module_section_file_path, 'r') as f:
            module_file = json.load(f)
        if module_file['module'] not in self.flow_obj_dict:
            self.log.error(f"Module {module_file['module']} does not support the creation of climbs (yet). STOP.")
            exit(-1)
        if module_section_file_path in climb_file['variants']:
            self.log.error(f"Module {module_file['module']} is already in this Climb. STOP.")
            exit(-1)
        # further checks?
        climb_file['variants'].append(module_section_file_path)
        with open(climb_file_path, 'w') as f:
            json.dump(climb_file, f)

    def add_file(self, file_path, language, climb_file_path):
        climb_file_path = _harmonizing_climb_file_path(climb_file_path)
        if language not in __supported_languages__:
            self.log.error(f"Language {language} is currently not supported. STOP.")
            exit(-1)
        with open(climb_file_path, 'r') as f:
            climb_file = json.load(f)
        nt = (os.path.abspath(file_path), language)
        for tp in climb_file['main_files']:
            if nt[0] == tp[0]:
                self.log.error(f"File {nt[0]} is already in this Climb. STOP.")
                exit(-1)
        climb_file['main_files'].append(nt)
        # further checks?
        with open(climb_file_path, 'w') as f:
            json.dump(climb_file, f)

    def emit(self, climb_file_path, out_dir=None):
        climb_file_path = _harmonizing_climb_file_path(climb_file_path)
        with open(climb_file_path, 'r') as f:
            climb_file = json.load(f)
        if out_dir is None:
            out_dir = climb_file['out_dir']
            self.log.warning(f"Using the output directory: {out_dir}")
        out_dir_path = os.path.abspath(out_dir)
        os.system(f"mkdir -p {out_dir_path}")
        if len(climb_file['main_files']) < 1:
            self.log.error("At least one main source file needs to be specified before a Climb can be emitted. STOP.")
            exit(-1)
        if len(climb_file['variants']) < 1:
            self.log.error("At least one variant/module needs to be specified before a Climb can be emitted. STOP.")
            exit(-1)

        variants = {}
        files_to_copy = []
        install_notes = {}
        for vp in climb_file['variants']:
            with open(vp, 'r') as f:
                module_file = json.load(f)
            mod_name = module_file['module']
            variants[mod_name] = module_file
            dir_path = os.path.dirname(vp)
            for fp in module_file['relative_files_dirs_to_copy']:
                # np = os.path.abspath(os.path.relpath(fp, vp))
                np = os.path.abspath(os.path.join(dir_path, fp))
                files_to_copy.append(np)
                os.system(f"cp -R {np} {out_dir_path}/{fp}")
            notes = self.flow_obj_dict[mod_name].get_install_notes()
            if notes is not None:
                install_notes[mod_name] = notes

        # margot files
        os.system(f"cp {os.path.abspath(os.path.join(__filedir__, 'lib/margot.json'))} {out_dir_path}")
        os.system(f"cp {os.path.abspath(os.path.join(__filedir__, 'lib/ops.json'))} {out_dir_path}")

        dockerfile_present = False
        for tp in climb_file['main_files']:
            mf_path = tp[0]
            mf_lang = tp[1]
            if 'Dockerfile' in mf_path:
                dockerfile_present = True
            if mf_lang == 'copy':
                os.system(f"cp -R {mf_path} {out_dir_path}")
            elif mf_lang in __supported_programming_languages__:
                out_file_path = os.path.abspath(os.path.join(out_dir_path, os.path.basename(mf_path)))
                lines_to_accelerate = []
                record_lines = False
                init_args_dict = {}
                accelerate_args_dict = {}
                runtime_code_necessary = False
                runtime_append_code = ''
                with open(os.path.abspath(mf_path), 'r') as in_file, \
                        open(os.path.abspath(out_file_path), 'w') as out_file:
                    for line in in_file.readlines():
                        if '@basecamp climbs init' in line:
                            indent = ' ' * (len(line) - len(line.lstrip()))
                            outline = f'{indent}{get_comment_string(mf_lang)}\n'
                            args_dict = {}
                            if 'args=' in line:
                                ds = line.split("args=")[1].rstrip()
                                args_dict = json.loads(ds)
                            init_args_dict = args_dict
                            for vi, vsection in variants.items():
                                init_format_dict = vsection['init_format_dict']
                                init_format_dict.update(args_dict)
                                init_code = self.flow_obj_dict[vi].get_init_code(init_format_dict, mf_lang)
                                if init_code == -1:
                                    continue
                                init_code_lines = init_code.splitlines()
                                for l in init_code_lines:
                                    outline += f'{indent}{l}\n'
                                outline += '\n'
                        elif '@basecamp climbs accelerate begin' in line:
                            # indent = len(line) - len(line.lstrip())
                            accelerate_args_dict = {}
                            lines_to_accelerate = []
                            if 'args=' in line:
                                ds = line.split("args=")[1].rstrip()
                                accelerate_args_dict = json.loads(ds)
                            record_lines = True
                            outline = 'delme'
                        elif '@basecamp climbs accelerate end' in line:
                            record_lines = False
                            runtime_code_necessary = True
                            runtime_append_code = f'\n{get_comment_string(mf_lang)}\n'  # to avoid duplications
                            indent = ' ' * (len(line) - len(line.lstrip()))
                            outline = f'{indent}{get_comment_string(mf_lang)}\n'
                            # drop first
                            lines_to_accelerate = lines_to_accelerate[1:]
                            variant_lines = [lines_to_accelerate]  # list of lists
                            runtime_variant_checks = [None]
                            files_to_append = []
                            for vi, vsection in variants.items():
                                run_format_dict = vsection['run_format_dict']
                                run_format_dict.update(accelerate_args_dict)
                                run_code = self.flow_obj_dict[vi].get_run_code(run_format_dict, mf_lang)
                                if run_code == -1:
                                    continue
                                if vi in self.flow_language_wrappers_check[mf_lang]:
                                    fapp, signature = self.flow_language_wrappers_check[mf_lang][vi]
                                    files_to_append.append(fapp)
                                    runtime_variant_checks.append(signature)
                                run_code_lines = run_code.splitlines()
                                ll = []
                                for l in run_code_lines:
                                    ll.append(f'{indent}{l}')
                                variant_lines.append(ll)
                            # now, generate variant code
                            all_args_dict = init_args_dict
                            all_args_dict.update(accelerate_args_dict)
                            code_to_insert, code_to_append = self.generate_margot_instantiation(mf_lang, indent,
                                                                                           all_args_dict, variant_lines,
                                                                                           runtime_variant_checks,
                                                                                           files_to_append)
                            outline += code_to_insert
                            runtime_append_code += code_to_append
                        else:
                            outline = line
                        if record_lines:
                            lines_to_accelerate.append(outline)
                        else:
                            out_file.write(outline)
                    if runtime_code_necessary:
                        out_file.write(runtime_append_code)

        # emit build instructions
        with open(os.path.join(out_dir_path, 'basecamp_build_and_run_instructions.md'), 'w') as out_file:
            out_file.write(f"Build and run instructions for the EVEREST accelerated app: {climb_file['name']}\n"
                           f"============================================================="
                           f"{'='*len(climb_file['name'])}\n\n")
            out_file.write('\nBuild:\n'
                           '-------\n\n')
            # margot dependencies
            out_file.write("For the runtime tuner:\n```bash\n"
                           "sudo snap install mosquitto  # or other ways: https://mosquitto.org/download/\n"
                           "docker pull margotpolimi/brian:1.0\n"
                           "docker pull margotpolimi/stub_agora:1.0\n"
                           "```\n")
            if dockerfile_present:
                app_name = f"ebc_accelerated_{climb_file['name'].replace(' ', '')}"
                out_file.write("\nApparently, the app has it's own Dockerfile, so maybe:\n```bash\n"
                               f"docker build -f Dockerfile -t {app_name}:latest .\n"
                               "```\n")

            if len(install_notes) > 0:
                out_file.write("Furthermore, the following modules have specific installation instructions:\n")
                for mod, notes in install_notes.items():
                    out_file.write(f"- **{mod}**:\n{notes}\n")
            out_file.write('\nRun:\n'
                           '-------\n\n')
            out_file.write("For the runtime tuner:\n```bash\n"
                           "docker run -d --rm --network host --name brian margotpolimi/brian:1.0\n"
                           "docker run -d --rm --network host --name stub_agora margotpolimi/stub_agora:1.0\n"
                           "mosquitto_pub -t agora/traffic^0.1^block1/knowledge -f ops.json\n"
                           "```\n")
            if dockerfile_present:
                out_file.write("\nTo start the app container, maybe:\n```bash\n"
                               f"docker run --rm --network host -it --name {app_name}\n```\n")
            out_file.write("\nHappy EVEREST climbing!\n\n")

    def generate_margot_instantiation(self, language, local_indent, all_args_dict, variant_lines, runtime_variant_checks,
                                      files_to_append):
        if language != 'python':
            self.log.error("The call to different variants at runtime using margot is currently only supported in "
                           "python. STOP")
            exit(-2)

        __select_variant_function_name__ = 'margot_select_variant'
        variant_selection_wrapper = f'def {__select_variant_function_name__}():\n'
        for i, check in enumerate(runtime_variant_checks):
            if check is None:
                continue
            outline = f'    if {check.format_map(all_args_dict)}:\n        return {i}\n'
            variant_selection_wrapper += outline
        variant_selection_wrapper += '    return 0\n'

        code_to_append = Path(os.path.abspath(os.path.join(__filedir__, 'lib/margot_init.py'))).read_text()
        code_to_append += '\n'
        code_to_append += variant_selection_wrapper
        code_to_append += '\n'

        for fp in files_to_append:
            cta = Path(os.path.abspath(fp)).read_text()
            code_to_append += cta
            code_to_append += '\n'

        __accelerate_function_name__ = 'everest_accelerate'
        margot_call_code = f'{local_indent}import time\n\n'
        margot_call_code += f'{local_indent}@tune(tuner,\n' \
                            f'{local_indent}      knobs=[{{"name": "version", "type": "int"}}],\n' \
                            f'{local_indent}      metrics=[{{"name": "time", "function": extract_time}}],\n' \
                            f'{local_indent}      features=[{{"name": "hw", "function": ' \
                            f'{__select_variant_function_name__}}}])\n'
        margot_call_code += f'{local_indent}def {__accelerate_function_name__}(version = 0):\n' \
                            f'{local_indent}    start = time.time()\n{local_indent}    try:\n'
        current_indent = f'{local_indent}        '
        for i, lines in enumerate(variant_lines):
            margot_call_code += f'{current_indent}if variant == {i}:\n'
            current_indent += '    '
            for l in lines:
                if len(l.lstrip().rstrip()) == 0:
                    continue
                margot_call_code += f'{current_indent}{l.lstrip().rstrip()}\n'
            current_indent = current_indent[:-4]
        margot_call_code += f'{local_indent}    except:  # fallback to cpu version\n'
        current_indent = f'{local_indent}        '
        # index 0 is basis version
        for l in variant_lines[0]:
            if len(l.lstrip().rstrip()) == 0:
                continue
            margot_call_code += f'{current_indent}{l.lstrip().rstrip()}\n'
        margot_call_code += f'{local_indent}    end = time.time()\n{local_indent}    return end-start\n\n'

        margot_call_code += f'{local_indent}{__accelerate_function_name__}()\n\n'

        return margot_call_code, code_to_append

    def create_module_section(self, flow, init_format_dict, run_format_dict, relative_files_dirs_to_copy, out_dir_path):
        section_file = __section_file_template__.copy()
        section_file['module'] = flow.flow_identifier
        section_file['init_format_dict'] = init_format_dict
        section_file['run_format_dict'] = run_format_dict
        section_file['relative_files_dirs_to_copy'] = relative_files_dirs_to_copy
        out_file = os.path.abspath(os.path.join(out_dir_path, f'{flow.flow_identifier}.section'))
        with open(out_file, 'w') as f:
            json.dump(section_file, f)

