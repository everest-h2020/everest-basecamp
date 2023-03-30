
import json
import os
import sys
from docopt import docopt

from ebc import basecamp

__version__ = 0.1


arguments = docopt(basecamp.docstr, version=__version__)
basecamp.cli(arguments)

