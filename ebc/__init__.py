
import sys
import logging

from basecamp import EverestBasecamp

# if __name__ == '__main__':
# vitrualenv is activated by the bash script
if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
    # This works with virtualenv for Python 3 and 2 and also for the venv module in Python 3
    print("[ebc:ERROR] It looks like this sra isn't running in a virtual environment. STOP.")
    sys.exit(1)

FORMAT = '%(levelname)-9s %(threadName)-30s %(name)-30s: %(funcName)-20s %(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT)

ebc = EverestBasecamp
