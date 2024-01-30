
from .climbs import Climbs, __supported_languages__

module = Climbs
identifier = 'climbs'

docstrs = {'usage': 'climbs (describe --flow <flow> | '
                    'create --name <name> <path-to-file.climb> | '
                    'add_module --module <path-to-module.section> <path-to-file.climb> | '
                    'add_file --file <path-to-source.file> --language <language> <path-to-file.climb> | '
                    'emit <path-to-file.climb> [--output-directory <path-to-output-directory>])',
           'commands': ('climbs', 'Combines different flows (i.e. "everest climbs") to one application.'),
           'options': [
               ('describe', 'Describes the required API for the flow.'),
               ('--flow <flow>', 'Specifies the flow to describe.'),
               ('create', 'Create a new flow.'),
               ('add_module --module', 'Add a new application variant to an existing climb.'),
               ('add_file --file', 'Add file (with annotations) of the main application to the climb.'),
               ('--language <language>', f'The langauge of the added file. Currently supported are: '
                                         f'{", ".join(__supported_languages__)}. '
                                         f'(Copy means the file will be copied without change.)'),
               ('emit', 'Emit created climb to build directory.')
           ]}
