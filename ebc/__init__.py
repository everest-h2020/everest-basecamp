
import sys
import logging

from .everest_basecamp import EverestBasecamp

if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
    # This works with virtualenv for Python 3 and 2 and also for the venv module in Python 3
    print("[ebc:ERROR] It looks like this basecamp isn't running in a virtual environment. STOP.")
    sys.exit(1)

FORMAT = '%(levelname)-9s %(threadName)-15s %(name)-15s: %(funcName)-15s %(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level='WARNING')

basecamp = EverestBasecamp()
