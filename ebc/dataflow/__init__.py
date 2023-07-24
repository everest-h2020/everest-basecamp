
from .ohua import Ohua

module = Ohua
identifier = 'dataflow'

docstrs = {'usage': 'dataflow <input-file> -o <path-to-output> --target <target> --threads <num> '
                    '--enable-parallelism <bool> --c-limit <num> --amorphous <bool> '
                    '--ohuac <path-to-ohuac>',
           'commands': ('dataflow', 'Invokes the dataflow flow of the EVEREST SDK.'),
           'options': [
               ('-o <path-to-output>', 'Path to save generated files under (defualts to `generated`).'),
               ('--target <target>', 'Target for the code generator (supported values: rust, mlir).'),
               ('--threads <num>', 'Number of threads to parallelize for (default: number of local cores).'),
               ('--enable-parallelism <bool>', 'Whether to enable the parallelization optimization (defaults to `true`).'),
               ('--c-limit <num>', 'Number of maximum collisions for a computation with amorphous data parallelism.'),
               ('--amorphous <bool>', 'Whether to enable the transformation of amorphous data parallel tasks (defaults to `false`).'),
               ('--ohuac <path-to-ohuac>', 'ohuac binary to use. Can be omitted if `ohuac` is in your path.')
            ]}
