
from .inference import Emli

module = Emli
identifier = 'ml-inference'

docstrs = {'usage': 'ml-inference (--json-constraints <path-to-json-constraints> | --app-name <app-name> '
                    '--target-throughput <target-sps> --batch-size <batch-size> --used_bit_width <used-bit-width> '
                    '--onnx-input-name <onnx-input-name> --onnx-input-shape <onnx-input-shape>) '
                    '[--map-weights <path-to-weights-file>] onnx|torchscript'
                    '<path-to-onnx> <path-to-output-directory> [--calibration-data <path-to-calibration-data>]',
           'commands': ('ml-inference', 'Invokes the ML inference flow of the EVEREST SDK.'),
           'options': [
               ('--json-constraints <path-to-json-constraints>', 'Imports the ML target constraints of the given JSON file.'),
               ('--app-name <app-name>', 'The name of the target application (to create human readable lables).'),
               ('--target-throughput <target-sps>', 'The targeted throughput (in samples-per-second (sps) of the inference application.'),
               ('--batch-size <batch-size>', 'The used batch size per inference request (i.e. sample).'),
               ('--used_bit_width <used-bit-width>', 'The bit width to use for input, activations, and weights.'),
               ('--onnx-input-name <onnx-input-name>', 'The name of the input node in the ONNX graph.'),
               ('--onnx-input-shape <onnx-input-shape>', 'The shape of the input in the ONNX graph.'),
               ('--map-weights <path-to-weights-file>', 'The file containing the weights for the kernel-weight-mapping schema.'),
               ('--calibration-data <path-to-calibration-data>', 'Points to the .npy file containing example data to calibrate transformation to quantized data types.')
           ]}

climbing = {
    'description_path': 'ml/lib/describe.md',
    'run': {
        'python': 'ml/lib/invoke.py'
    },
    'init': {
        'python': 'ml/lib/init.py',
        'docker': 'ml/lib/dockerfile_init',
    },
    'runtime_check': {
        # path, signature to call (format string)
        'python': ('ml/lib/check.py', 'check_cf_action_ready({action_name})')
    }
}

# TODO: run and init code better via getter of the flow module?
#  so that e.g. precision can be inserted etc?
#  the arg dict is given as argument (and the detected indent)
#  check still as file and signature
