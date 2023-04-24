everest-basecamp
========================
The basis for all EVEREST endeavors.

`everest-basecamp` is the facade compiler for the Everest System Development Kit.



Usage:
```bash
$ ./ebc-cli -h
EVEREST basecamp -- the basis for all EVEREST endeavors.

Usage:
    ebc-cli dataflow <whatever>
    ebc-cli hpc <whatever>
    ebc-cli ml-inference (--json-constraints <path-to-json-constraints> | --app-name <app-name> --target-throughput <target-sps> --batch-size <batch-size> --used_bit_width <used-bit-width> --onnx-input-name <onnx-input-name> --onnx-input-shape <onnx-input-shape>) [--map-weights <path-to-weights-file>] <path-to-onnx> <path-to-output-directory>
    ebc-cli automatic <whatever>
    ebc-cli -h|--help
    ebc-cli -v|--version

Commands:
    dataflow                                          Invokes the dataflow flow of the EVEREST SDK.
    hpc                                               Invokes the HPC flow of the EVEREST SDK.
    ml-inference                                      Invokes the ML inference flow of the EVEREST SDK.
    automatic                                         Invokes the automatic flow detection feature.

Options:
    -h --help                                         Show this screen.
    -v --version                                      Show version.

    --json-constraints <path-to-json-constraints>     Imports the ML target constraints of the given JSON file.
    --app-name <app-name>                             The name of the target application (to create human readable lables).
    --target-throughput <target-sps>                  The targeted throughput (in samples-per-second (sps) of the inference application.
    --batch-size <batch-size>                         The used batch size per inference request (i.e. sample).
    --used_bit_width <used-bit-width>                 The bit width to use for input, activations, and weights.
    --onnx-input-name <onnx-input-name>               The name of the input node in the ONNX graph.
    --onnx-input-shape <onnx-input-shape>             The shape of the input in the ONNX graph.
    --map-weights <path-to-weights-file>              The file containing the weights for the kernel-weight-mapping schema.

Copyright EVEREST Consortium, licensed under the Apache License 2.0.
For contact and more details please visit: https://everest-h2020.eu

```

## Setup
..todo...
```
cp ../../cloudFPGA/DOSA/setup/_virtualenv_path_extensions.pth ./venv2/lib/python3.8/site-packages/
python -m ipykernel install --user --name='venv2-ebc' --display-name='EVEREST basecamp (venv2)'
```

