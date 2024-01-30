Everest for LEXIS Airflow wrapper
===============================================

The airflow wrapper module requires some specific python dependencies. Also, `py4lexis` requires python>=3.10. 

```bash
# virtualenv of everest-basecamp should be activated
$ pip install -r ebc/aiflow/requirements.txt
```

For further details, please refer to the `py4lexis` documentation: https://opencode.it4i.eu/lexis-platform/clients/py4lexis

to use this environment in a jupyter notebook, execute
```bash
# with virutalenv activated
$ python -m ipykernel install --user --name='venv-ebc' --display-name='EVEREST basecamp (venv)'
```



