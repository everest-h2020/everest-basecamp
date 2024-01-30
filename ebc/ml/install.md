Everest ML inference (EMLI) setup guide
===============================================

For the machine learning inference module of the everest basecamp tool, some *additional* setup steps are required.

1. The EMLI flow depends on the DOSA tools, so a complete installation of DOSA is required (please refer to the setup instructions of DOSA). 
2. After DOSA is installed, the following steps are necessary to use DOSA within the basecamp tool: 
```bash
# virtualenv of everest-basecamp should be activated
$ pip install -r ebc/ml/requirements.txt --no-dependencies
$ cp <DOSA-repository>/setup/_virtualenv_path_extensions.pth ./path/to/ebc-virtualenv/lib/python3.8/site-packages/
# or, copy directly <DOSA-repository>/venv/lib/python3.8/site-packages/__virtualenv_path_extensions.pth
$ cd ebc/ml
$ cp config.json.sample config.sample  # adapt the paths in config.sample to point to the local DOSA installation
```

to use this environment in a jupyter notebook, execute
```bash
# with virtualenv activated
$ python -m ipykernel install --user --name='venv-ebc' --display-name='EVEREST basecamp (venv)'
```



