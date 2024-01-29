
from adam_python.wrapper import tune
from adam_python.interface import Tuner

tuner = Tuner(json_loc="./margot.json", broker_ip="127.0.0.1", seed="request")
