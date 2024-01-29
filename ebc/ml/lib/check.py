###############################################
# this code is required to check if an FPGA cluster
#  to be used by DOSA is available
import os
import json
import requests

__filedir__ = os.path.dirname(os.path.abspath(__file__))
__openstack_user_template__ = {'credentials': {'username': "your user name", 'password': "your user password"},
                               'project': "default"}
__cf_manager_url__ = "10.12.0.132:8080"
__NON_FPGA_IDENTIFIER__ = "NON_FPGA"
__rank_calling_FPGA_resets__ = 0


def errorReqExit(msg, code):
    print("Request " + msg + " failed with HTTP code " + str(code) + ".\n")
    exit(1)


def load_user_credentials(json_file):
    __openstack_user__ = 'X'
    __openstack_pw__ = 'Y'
    __openstack_project__ = 'Z'

    try:
        with open(json_file, 'r') as infile:
            data = json.load(infile)
        __openstack_user__ = data['credentials']['username']
        __openstack_pw__ = data['credentials']['password']
        if 'project' in data:
            __openstack_project__ = data['project']
        ret_dict = {'user': __openstack_user__, 'pw': __openstack_pw__, 'proj': __openstack_project__}
        return 0, ret_dict
    except Exception as e:
        print(e)
        print("Writing credentials template to {}\n".format(json_file))

    with open(json_file, 'w') as outfile:
        json.dump(__openstack_user_template__, outfile)
    return -1, {}


def get_action_data(action_name, user_dict):
    print("Requesting action data...")

    r1 = requests.get("http://" + __cf_manager_url__ + "/actions/" + str(action_name) + "?username={0}&password={1}"
                      .format(user_dict['user'], user_dict['pw']))

    if r1.status_code != 200:
        # something went horrible wrong
        return errorReqExit("GET action", r1.status_code)

    action_data = json.loads(r1.text)
    return action_data


def check_cf_action_ready(action_name, json_file='./user.json') -> bool:
    _, user_dict = load_user_credentials(json_file)
    action = get_action_data(action_name, user_dict)
    # print(action)
    if len(action['deployed_cluster_ids']) == 0:
        print("ERROR: Requested action is not defined.\nFAILED DEPENDENCY. STOP.")
        exit(1)
    return len(action['deployed_cluster_ids']) >= 1

###############################################

