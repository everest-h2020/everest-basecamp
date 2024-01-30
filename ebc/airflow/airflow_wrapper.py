import sys
import os
import json
from pathlib import Path

from ebc.flow_module import BasecampFlowModule
# from ebc.climb_module import BasecampClimbModule
# from ebc.climbs.climbs import Climbs, __from_pragma_string__

__filedir__ = os.path.dirname(os.path.abspath(__file__))


class AirflowWrapper(BasecampFlowModule):
    def __init__(self, identifier):
        super().__init__(identifier)
        # self._initialized_machine_specific = False
        self._lexis_session = None
        self._airflow_obj = None

    def _init_lexis_session_if_required(self):
        from py4lexis.session import LexisSession
        from py4lexis.workflows.airflow import Airflow
        if self._lexis_session is None:
            self._lexis_session = LexisSession()
            # reset airflow obj
            self._airflow_obj = None
        if self._airflow_obj is None:
            self._airflow_obj = Airflow(self._lexis_session)

    def cli(self, args, config):
        # print(args)
        # print_response always True, so it is the "CLI mode"
        if args['create']:
            self.create(args['<workflow-name>'], True)
        if args['get_params']:
            self.get_params(args['<workflow-name>'], True)
        if args['execute']:
            wf_params = None
            if args['--params-json-path'] is not None:
                with open(os.path.abspath(args['--params-json-path']), 'r') as f:
                    wf_params = json.load(f)
            self.execute(args['<workflow-name>'], wf_params, True)
        if args['get_state']:
            self.get_state(args['<workflow-name>'], True)

    def compile(self, **kwargs):
        self.log.warning("forwarding to `execute` command...")
        self.execute(**kwargs)

    def create(self, wf_name, print_response=False):
        raise NotImplementedError

    def get_params(self, wf_name, print_response=False):
        self._init_lexis_session_if_required()
        wf_params = self._airflow_obj.get_workflow_params(wf_name)
        if print_response:
            print(json.dumps(wf_params, indent=4))
        return wf_params

    def get_state(self, wf_name, print_response=False):
        self._init_lexis_session_if_required()
        wf_states = self._airflow_obj.get_workflow_states(wf_name)
        if print_response:
            print(json.dumps(wf_states, indent=4))
        return wf_states

    def execute(self, wf_name, wf_params=None, print_response=False):
        self._init_lexis_session_if_required()
        if wf_params is None:
            wf_params = self.get_params(wf_name)
        post_response = self._airflow_obj.execute_workflow(wf_name, wf_params)
        if print_response:
            print(json.dumps(post_response, indent=4))
        return post_response

