import sys
import os
import json

from ebc.flow_module import BasecampFlowModule
from ebc.climb_module import BasecampClimbModule
from ebc.climbs.climbs import Climbs, __from_pragma_string__

__filedir__ = os.path.dirname(os.path.abspath(__file__))
__default_dosa_config_path__ = os.path.abspath(os.path.join(__filedir__, 'dosa_config_default.json'))
__constraint_template_path__ = os.path.abspath(os.path.join(__filedir__, 'meta_template.json'))
__config_json__ = os.path.abspath(os.path.join(__filedir__, 'config.json'))
__arch_gen_strategies__ = ['performance', 'resources', 'default', 'latency', 'throughput']
__tmp_constraint_json__ = '/tmp/ecb-dosa-constraints.json'
__tmp_dosa_config_json__ = '/tmp/ecb-dosa-config.json'


class Emli(BasecampFlowModule, BasecampClimbModule):

    def __init__(self):
        super().__init__()
        self._initialized_machine_specific = False
        with open(__default_dosa_config_path__, 'r') as inp:
            self.dosa_config = json.load(inp)
        with open(__constraint_template_path__, 'r') as inp:
            self.app_constraints = json.load(inp)
        self.constraints_set = False
        self.used_flow = None
        self.model_path = None
        self.pytorch_module = None
        self.model_set = False
        self.output_path = None
        self.map_weights = None
        self.calibration_data = None
        self.disable_roofline_gui = False
        self.disable_build = False
        self.dosa_dir = None
        self.dosa_envs = {}
        self.climb_obj = None

    def _load_machine_specific_files(self):
        with open(__config_json__, 'r') as inp:
            module_config = json.load(inp)
        self.log.info(f"[ML inference module] using the module configuration at {__config_json__}.")
        # self.dosa_exec = os.path.abspath(os.path.join(__filedir__, module_config['exec_path']))
        # TODO: update if DOSA is a submodule...then path will be not machine/installation dependent
        # self.dosa_main = os.path.abspath(os.path.join(__filedir__, module_config['main_path']))
        # self.dosa_venv = os.path.abspath(os.path.join(__filedir__, module_config['venv_path']))
        # self.dosa_dir = os.path.dirname(self.dosa_exec)
        # self.dosa_dir = os.path.dirname(self.dosa_venv)
        self.dosa_dir = os.path.abspath(os.path.join(__filedir__, module_config['dosa_dir_path']))
        envs = module_config['env_vars']
        self.dosa_envs = {}
        self.dosa_envs.update(envs)
        self._initialized_machine_specific = True

    def _call_dosa(self):
        if not self._initialized_machine_specific:
            self._load_machine_specific_files()
        # cmd = f'source {self.dosa_venv}/bin/activate; '
        # for k, v in self.dosa_envs.items():
        #     cmd += f'export {k}={v}; '
        #     os.environ[k] = v
        # cmd += f'export PYTHONPATH={self.dosa_dir}; '
        # # cmd += f'cd {self.dosa_dir}; '
        # # cmd += self.dosa_exec
        # cmd += f'python3 {self.dosa_main}'

        # add args
        with open(__tmp_dosa_config_json__, 'w') as outp:
            json.dump(self.dosa_config, outp)
        with open(__tmp_constraint_json__, 'w') as outp:
            json.dump(self.app_constraints, outp)
        model_abspath = os.path.abspath(os.path.join(__filedir__, self.model_path))
        dosa_args = f'{__tmp_dosa_config_json__} {self.used_flow} {model_abspath} {__tmp_constraint_json__} ' \
                    f'{os.path.abspath(self.output_path)}'
        if self.calibration_data is not None:
            dosa_args += f' --calibration-data {self.calibration_data}'
        if self.disable_roofline_gui:
            dosa_args += ' --no-roofline'
        elif self.disable_build:
            dosa_args += ' --no-build'

        # cmd += ' ' + dosa_args
        # self.log.debug(f"DOSA command: {cmd}")
        # os.system(cmd)
        # subprocess.run(cmd, shell=True, stdin=sys.stdin.fileno(), stdout=sys.stdout.fileno(),
        #                stderr=sys.stderr.fileno())
        self.log.debug(f"calling DOSA... (with args: {dosa_args}).")
        self.log.debug(f"trying to import DOSA from {self.dosa_dir}.")
        sys.path.insert(0, self.dosa_dir)
        from gradatim import dosa, DosaModelType
        """
        def dosa(dosa_config_path, model_type: DosaModelType, model_path: str, const_path: str, global_build_dir: str,
                 show_graphics: bool = True, generate_build: bool = True, generate_only_stats: bool = False,
                 generate_only_coverage: bool = False, calibration_data: str = None):
        """
        generate_build = not self.disable_build
        show_graphics = not self.disable_roofline_gui
        model_type = DosaModelType.ONNX
        if self.used_flow == 'torchscript':
            model_type = DosaModelType.TORCHSCRIPT
        dosa(__tmp_dosa_config_json__, model_type, model_abspath, __tmp_constraint_json__, os.path.abspath(self.output_path),
             show_graphics=show_graphics, generate_build=generate_build, calibration_data=self.calibration_data)

    def compile(self, **kwargs):
        if not self._initialized_machine_specific:
            self._load_machine_specific_files()
        # TODO: do we need kwargs?
        # if not self.constraints_set or (self.onnx_path is None and self.pytorch_module is None) \
        #     or self.output_path is None:
        if not self.constraints_set:
            err_msg = 'Constraints are not set. STOP.'
            self.log.error(err_msg)
            return err_msg
        if not self.model_set:
            err_msg = 'DNN model not set. STOP.'
            self.log.error(err_msg)
            return err_msg
        if self.output_path is None:
            err_msg = 'Output path not set. STOP.'
            self.log.error(err_msg)
            return err_msg
        self._call_dosa()
        # TODO
        self.climb_obj.create_module_section()

    def cli(self, args, config):
        if not self._initialized_machine_specific:
            self._load_machine_specific_files()
        if args['--json-constraints'] is not None:
            with open(args['--json-constraints'], 'r') as inp:
                json_dict = json.load(inp)
            self.set_constraint_dict(json_dict)
        else:
            # we don't need to check the "correctness" that's done by docopt
            precision = args['--used_bit_width']
            self.set_constraints(app_name=args['--app-name'],
                                 onnx_input_name=args['--onnx-input-name'],
                                 input_shape=args['--onnx-input-shape'],
                                 input_size_t=precision,
                                 bitwidth_of_activations=precision,
                                 bitwidth_of_weights=precision,
                                 batch_size=args['--batch-size'],
                                 target_throughput=args['--target-throughput'],
                                 arch_gen_strategy='throughput'
                                 )
        if args['--map-weights'] is not None:
            self.log.error("Kernel-mapping schema is NOT YET IMPLEMENTED.")
            return -1
        self.set_output_path(args['<path-to-output-directory>'])
        used_flow = None
        if args['onnx']:
            used_flow = 'onnx'
        elif args['torchscript']:
            used_flow = 'torchscript'
        self.set_model_path(used_flow, args['<path-to-onnx>'])
        self.calibration_data = args['<path-to-calibration-data>']
        self.compile()
        return 0

    def get_constraints(self):
        return self.app_constraints

    def set_constraint_dict(self, new_constraints_dict):
        self.app_constraints = new_constraints_dict
        self.constraints_set = True
        return 0

    def set_constraints(self, app_name, onnx_input_name, input_shape, input_size_t,
                        batch_size, arch_gen_strategy, target_throughput=-1, target_latency=-1,
                        resource_budget=-1, quantization='none', bitwidth_of_weights=None, bitwidth_of_activations=None):
        if target_throughput == -1 and target_latency == -1 and resource_budget == -1:
            err_msg = "Either target_throughput, target_latency, or resource_budget must be defined. STOP."
            self.log.error(err_msg)
            return err_msg
        if arch_gen_strategy not in __arch_gen_strategies__:
            err_msg = f"{arch_gen_strategy} is not a valid strategy. STOP."
            self.log.error(err_msg)
            return err_msg
        # TODO
        # if bitwidth_of_input != bitwidth_of_weights:
        #     self.log.error("NOT YET IMPLEMENTED: input and data must have the same bitwidths. STOP.")
        #     return -1
        self.app_constraints['name'] = app_name
        self.app_constraints['shape_dict'] = {onnx_input_name: input_shape}
        self.app_constraints['used_input_size_t'] = input_size_t
        self.app_constraints['quantization'] = quantization
        if (quantization == 'none') and (bitwidth_of_weights is not None and bitwidth_of_activations is not None):
            overwrite_dtypes = {'data': f'int{bitwidth_of_activations}', 'weights': f'int{bitwidth_of_weights}',
                                'fixed_point_fraction_bits': bitwidth_of_weights - 1, 'accum_bits_factor': 2}
            self.app_constraints['overwrite_dtypes'] = overwrite_dtypes
        self.app_constraints['used_batch_n'] = batch_size
        self.app_constraints['target_sps'] = target_throughput
        self.app_constraints['target_latency'] = target_latency
        self.app_constraints['target_resource_budget'] = resource_budget
        # TODO
        # self.app_constraints['targeted_hw'] =
        # self.app_constraints['fallback_hw'] =
        self.app_constraints['arch_gen_strategy'] = arch_gen_strategy

        self.constraints_set = True
        return 0

    def set_output_path(self, output_path):
        self.output_path = os.path.abspath(output_path)

    def set_model_path(self, flow_type, model_path):
        assert flow_type == 'onnx' or flow_type == 'torchscript'
        self.model_path = os.path.abspath(model_path)
        self.used_flow = flow_type
        self.model_set = True

    def set_calibration_data_path(self, calibration_data_path):
        self.calibration_data = os.path.abspath(calibration_data_path)

    def get_run_code(self, args, language):
        pass

    def get_init_code(self, args, language):
        pass

    def set_climb_obj(self, climb_obj):
        self.climb_obj = climb_obj

