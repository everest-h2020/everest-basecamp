
from .airflow_wrapper import AirflowWrapper

module = AirflowWrapper
identifier = 'airflow'

docstrs = {'usage': f'{identifier} ( create | get_params | get_state | '
                    f'execute [--params-json-path <path-to-json-params>]) <workflow-name>',
           'commands': (f'{identifier}', 'Allows the executions of Airflow workflows via Py4Lexis.'),
                                         # '(this flow requires python>=3.10) .'),
           'options': [
               ('create', 'Create a new Airflow workflow.'),
               ('get_params', 'Get the current parameters of a workflow.'),
               ('get_state', 'Request the current state of a workflow.'),
               ('execute', 'Trigger the execution of a workflow.'),
               ('--params-json-path <path-to-json-params>', 'Optional update of workflow parameters for execution.')
           ]}
