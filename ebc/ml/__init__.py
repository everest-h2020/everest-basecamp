#  /*******************************************************************************
#   * Copyright 2022 -- 2024 EVEREST consortium (everest-h2020.eu)
#   *
#   * Licensed under the Apache License, Version 2.0 (the "License");
#   * you may not use this file except in compliance with the License.
#   * You may obtain a copy of the License at
#   *
#   *     http://www.apache.org/licenses/LICENSE-2.0
#   *
#   * Unless required by applicable law or agreed to in writing, software
#   * distributed under the License is distributed on an "AS IS" BASIS,
#   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   * See the License for the specific language governing permissions and
#   * limitations under the License.
#  *******************************************************************************/
#

from .inference import Emli

module = Emli
identifier = 'ml_inference'

docstrs = {'usage': 'ml_inference (onnx|torchscript) (--json-constraints <path-to-json-constraints> '
                    '| ( --app-name <app-name> --target-throughput <target-sps> --batch-size <batch-size> '
                    '--used_bit_width <used-bit-width> --onnx-input-name <onnx-input-name> '
                    '--onnx-input-shape <onnx-input-shape>)) '
                    '[--map-weights <path-to-weights-file>] '
                    '<path-to-model.file> <path-to-output-directory> '
                    '[--calibration-data <path-to-calibration-data>]'
                    ,
           'commands': ('ml_inference', 'Invokes the ML inference flow of the EVEREST SDK.'),
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
    'runtime_check': {
        # path, signature to call (format string)
        'python': ('ml/lib/check.py', 'check_cf_action_ready({action_name})')
    }
}
