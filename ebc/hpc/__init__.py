
from .cfdlang import Cfdlang

module = Cfdlang
identifier = 'hpc'

docstrs = {'usage': 'hpc [--lang <lang-id> --pipeline <pipeline> (-D <define>...) (-I <include>...)] <input> -o <path-to-output>',
           'commands': ('hpc', 'Invokes the HPC flow of the EVEREST SDK.'),
           'options': []}
