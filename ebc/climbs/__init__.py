
from .climbs import Climbs

module = Climbs
identifier = 'climbs'

docstrs = {'usage': 'climbs (describe --flow <flow>)|create|add|(emit --out <path-to-output-directory>) '
                    '<path-to-file.climb>',
           'commands': ('climbs', 'Combines different flows (i.e. "everest climbs") to one application.'),
           'options': [
               ('describe', 'Describes the required API for the flow.'),
               ('--flow <flow>', 'Specifies the flow to describe.'),
               ('create', 'Create a new flow.'),
               ('add', 'Add a new application variant to an existing flow.'),
               ('emit', 'Emit created climb to build directory.')
           ]}
