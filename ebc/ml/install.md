Everest ML inference (EMLI) setup guide
===============================================

For the machine learning inference module of the everest basecamp tool, some *additional* setup steps are required.
There are two options: 
1. Install DOSA within the same virtual environment. This option may restrict the usage of other basecamp flows but allows to use all existing features.
2. Invoke DOSA within a docker container. This option does not introduce more constraints on the environments, however, all GUI features will not work. 


1: Install DOSA within the same virtual environment
--------------------------------------------------------

1. The EMLI flow depends on the DOSA tools, so a complete installation of DOSA is required (please refer to the [setup instructions of DOSA](https://github.com/cloudFPGA/DOSA/blob/main/doc/Install.md)). 
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

2: Invoke DOSA within a Docker container
------------------------------------------

This option requires only a simple environment:
```bash
# virtualenv of everest-basecamp should be activated
$ pip install pyro4
$ cd ebc/ml
$ cp config.json.sample config.sample  # adapt the file as described below
```

Then, DOSA can be built as docker container: https://github.com/cloudFPGA/DOSA/blob/main/doc/Dockerfile

```commandline
cd DOSA/doc
docker build -f Dockerfile -t dosa-build .
```

If building for the cloudFPGA target, the required `Shell_STATIC.dcp` files (as described above) should then be mounted to the `/current_dcps/` folder inside the container.
Please refer to the [setup instructions of DOSA](https://github.com/cloudFPGA/DOSA/blob/main/doc/Install.md#docker) for more details.

Afterwards, enable the [Pyro library](https://pyro4.readthedocs.io/en/stable/index.html) as follows:
```commandline
docker run -it -v ./my_in_and_out_dir/:/scratch:Z -v ./folder_with_current_shell_STATIC/:/current_dcps/:Z dosa-build
# inside the container
python3 -m gradatim.pyro_server
```
This prints out a PYRO-URI that should be inserted into the `'dosa_pyro4_uri'` entry of the `config.json` file. **If using this feature, the `config.json` must not contain an entry named `dosa_dir_path`.** 

Now, the Python API and CLI of the basecamp ml_inference flow can be used as usual (just without the option to display a roofline plot etc.)
Please note, that paths to e.g. the constraint file etc. then must be `/scratch/path_to_file.json`. 

