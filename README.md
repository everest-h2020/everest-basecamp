everest-basecamp
========================
The basis for all EVEREST endeavors.

`everest-basecamp` is the facade compiler for the Everest System Development Kit.



Usage:
```bash
EVEREST basecamp -- the basis for all EVEREST endeavors.

Usage:
    ebc-cli dataflow <input-file> -o <path-to-output> --target <target> --threads <num> --enable-parallelism <bool> --c-limit <num> --amorphous <bool> 
    ebc-cli hpc [--lang <lang-id> --pipeline <pipeline> (-D <define>...) (-I <include>...)] <input> -o <path-to-output>
    ebc-cli ml_inference onnx|torchscript (--json-constraints <path-to-json-constraints> | --app-name <app-name> --target-throughput <target-sps> --batch-size <batch-size> --used_bit_width <used-bit-width> --onnx-input-name <onnx-input-name> --onnx-input-shape <onnx-input-shape>) [--map-weights <path-to-weights-file>] <path-to-model.file> <path-to-output-directory> [--calibration-data <path-to-calibration-data>]
    ebc-cli climbs (describe --flow <flow> | create --name <name> <path-to-file.climb> | add_module --module <path-to-module.section> <path-to-file.climb> | add_file --file <path-to-source.file> --language <language> <path-to-file.climb> | emit <path-to-file.climb> [--output-directory <path-to-output-directory>])
    ebc-cli airflow ( create | get_params | get_state | execute [--params-json-path <path-to-json-params>]) <workflow-name>
    ebc-cli -h|--help
    ebc-cli -v|--version

Commands:
    dataflow                                          Invokes the dataflow flow of the EVEREST SDK.
    hpc                                               Invokes the HPC flow of the EVEREST SDK.
    ml_inference                                      Invokes the ML inference flow of the EVEREST SDK.
    climbs                                            Combines different flows (i.e. "everest climbs") to one application.
    airflow                                           Allows the executions of Airflow workflows via Py4Lexis (this flow requires python>=3.10) .

Options:
    -h --help                                         Show this screen.
    -v --version                                      Show version.

    -o <path-to-output>                               Path to save generated files under (defualts to `generated`).
    --target <target>                                 Target for the code generator (supported values: rust, mlir).
    --threads <num>                                   Number of threads to parallelize for (default: number of local cores).
    --enable-parallelism <bool>                       Whether to enable the parallelization optimization (defaults to `true`).
    --c-limit <num>                                   Number of maximum collisions for a computation with amorphous data parallelism.
    --amorphous <bool>                                Whether to enable the transformation of amorphous data parallel tasks (defaults to `false`).
    --json-constraints <path-to-json-constraints>     Imports the ML target constraints of the given JSON file.
    --app-name <app-name>                             The name of the target application (to create human readable lables).
    --target-throughput <target-sps>                  The targeted throughput (in samples-per-second (sps) of the inference application.
    --batch-size <batch-size>                         The used batch size per inference request (i.e. sample).
    --used_bit_width <used-bit-width>                 The bit width to use for input, activations, and weights.
    --onnx-input-name <onnx-input-name>               The name of the input node in the ONNX graph.
    --onnx-input-shape <onnx-input-shape>             The shape of the input in the ONNX graph.
    --map-weights <path-to-weights-file>              The file containing the weights for the kernel-weight-mapping schema.
    --calibration-data <path-to-calibration-data>     Points to the .npy file containing example data to calibrate transformation to quantized data types.
    describe                                          Describes the required API for the flow.
    --flow <flow>                                     Specifies the flow to describe.
    create                                            Create a new flow.
    add_module --module                               Add a new application variant to an existing climb.
    add_file --file                                   Add file (with annotations) of the main application to the climb.
    --language <language>                             The langauge of the added file. Currently supported are: python, docker, copy. (Copy means the file will be copied without change.)
    emit                                              Emit created climb to build directory.
    create                                            Create a new Airflow workflow.
    get_params                                        Get the current parameters of a workflow.
    get_state                                         Request the current state of a workflow.
    execute                                           Trigger the execution of a workflow.
    --params-json-path <path-to-json-params>          Optional update of workflow parameters for execution.

Copyright EVEREST Consortium, licensed under the Apache License 2.0.
For contact and more details please visit: https://everest-h2020.eu
```

## Setup

The basecamp tool is still under development and therefore, there exist multiple ways to execute it. 
The basecamp tool has a modular architecture with separate setup requirements for each module and a *common* general requirements setup. 

### General requirements

Basic build  and development tools are required. Also, we need a python virtual environment: 

 ```bash
$ virtualenv venv -p /usr/bin/python3  ## at least python3.8, see special requirements of individual flows
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python -m ipykernel install --user --name='venv-ebc' --display-name='EVEREST basecamp (venv)'
```

Now you can use the `ebc` module in Python or interact with the ebc command line interface (`./ebc-cli`).

Furthermore, you can execute all Everest flows in notebooks by starting the JupyterLab server:

```bash
$ jupyter-lab
```
As execution Kernel, the previous specified `EVEREST basecamp (venv)` needs to be used.

### Module installations

The setup of the available modules (`ml`, `dataflow`, `hpc`) is independent of each other and the respective guides can be found in the module folders:

- [ML inference](./ebc/ml/install.md)
- [HPC](./ebc/hpc/install.md)
- [Dataflow](./ebc/dataflow/install.md)


(It is also possible to have different virtual environments for each module.)

## Module structure (for development)
This sections states the requirements for each module and is intended to be read by the *developers* of the individual modules: 

Basecamp is designed to give a unified experience to the user while keeping the dependencies between the modules minimal.
Therefore, the requirements for a basecamp module are short:
1. It must be in a subfolder within [`./ebc`](./ebc)
2. This subfolder must contain a `__init__.py` that contains three objects:
    - `identifier`: A string that is unique for this module and is following python variable name restrictions (i.e. it must start with a letter or underscore and consists only of letters, numbers, and underscores) (it is used as an attribute internally).
    - `docstrs`: A dictionary containing three entries to be used to construct the `docopt` string (i.e. the entries must follow the [docopt syntax](http://docopt.org)):
      - `usage`: *One* string in one line that describes the CLI for this module (in the `Usage:` part of the docopt).
      - `commands`: *One* tuple containing the command and its description (for the `Commands:` section of docopt).
      - `options`: A *list of tuples*, each containing the command and its description (for the `Options:` part). 
    - `module`: A variable that points to the module class, which must inherit from the [`BasecampFlowModule`](./ebc/flow_module.py) and implement the `cli` and `compile` methods.
3. Add the `import <folder-name>` statement at the top of the [everest_basecamp.py](./ebc/everest_basecamp.py) file (below the line `import individual modules below`).  


## Funding

> This research was supported by the Horizon 2020 EU Research & Innovation programme under GA No 957269 (EVEREST project).



