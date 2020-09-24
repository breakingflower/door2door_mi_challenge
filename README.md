# MI Challenge

This repository describes my implementation of the coding challenge after a first interview at Door2door Berlin. The project should be received via email in a zip container, or cloned from github [here](https://github.com/fl0r1s/door2door_mi_challenge). Additionally, the project can be built as a docker image.

## Structure

The project contains an `visualiser` and a `simulator` directory. The `simulator` directory is a clone of the simulator directory in the [github page](https://github.com/door2door-io/mi-code-challenge), with some changes as highlighted in the *Edits in simulator* paragraph.

## Edits in simulator

- `Simulator.path_to_stops` is set to `simulator/berlin_stops.geojson`. It would be better to not hardcode this, for example by using an environment variable.
- Added `simulator/__init__.py` to load the simulator as a module in the app directory.
- `simulator/requirements.txt` updated to match `pandas==1.0.1` due to import errors on version 1.1.2

## Mindmap

## Running the application

### Python environment

Setting up the python environment is done as follows:

```python
# make sure you have the right tools (assumes you have a working install of python)
pip install virtualenv-tools
# Initialize an empty venv that will exist in the current working directory as `venv`
python3 -m venv env
# enable the virtual environment
source env/bin/activate
# install simulator requirements
pip install -r simulator/requirements.txt
# install visualiser requirements
pip install -r visualiser/requirements.txt
```

### Python3

The app can be run from the project root

```shell
python app.py
```

### Jupyter notebook

A jupyter notebook is given `API-showcase-notebook.ipynb`.

To open this file the user should install jupyterlab:

```shell
pip install jupyterlab
```

Afterwards, the file can be shown using

```shell
jupyter notebook API-showcase-notebook.ipynb
```

### Docker

A docker image can be built from the project root:

```shell
docker build -t mi-code-challenge .
```

A container showcasing the project can be run with
```shell
docker run -rm mi-code-challenge
```

## Test definitions

