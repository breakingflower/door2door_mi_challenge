# MI Challenge

This repository describes my implementation of the coding challenge after a first interview at Door2door Berlin. The project should be received via email in a zip container, or cloned from github [here](https://github.com/fl0r1s/door2door_mi_challenge). Additionally, the project can be built as a docker image.

## Structure

The project contains `visualiser`, `simulator`, `webapp` and `utilities` modules.

The `simulator` module is a clone of the simulator directory in the [github page](https://github.com/door2door-io/mi-code-challenge), with some changes as highlighted in the *Edits in simulator* paragraph. The `visualiser` module is used to generate locally-stored visualisations, and the `webapp` module shows the results in a web interface made in Flask. A utilities module is used to read the static data files.

## Edits in simulator

- `Simulator.path_to_stops` is moved to be an instance variable.
- Added `simulator/__init__.py` to allow loading of the simulator as a module.
- `simulator/requirements.txt` are moved to `requirements.txt` and updated to match `pandas==1.0.1` due to import errors on version 1.1.2
- Return type of simulator is not jsonified, e.g. `get_random_points` returns a geodataframe.
- Sets a default coordinate system in the generated geodataframe: EPSG:4326 (WGS84). This is necessary for getting map tiles from contextily, which operates in the current version in EPSG:3857 - Web mercator.

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
# install requirements
pip install -r requirements.txt
```

### Python3

The app can be run from the project root

```shell
python app.py
```

A webserver will start on `localhost:5000`.

### Jupyter notebook

A jupyter notebook is given `API-showcase-notebook.ipynb` that walks through the each of the modules in the application seperately.

To open this file the user should install jupyterlab:

```shell
pip install jupyterlab
```

Afterwards, the file can be shown using

```shell
jupyter notebook API-showcase-notebook.ipynb
```

### Docker

A docker image (tested for amd64) can be built from the project root Dockerfile:

```shell
docker build -t mi-code-challenge .
```

A container showcasing the project can be run with

```shell
docker run --rm -p 5000:5000 --name mi-code-challenge mi-code-challenge
```

Where we forward port 5000 from the container to localhost. The name of the container is set to `mi-code-challenge`.

The docker image can also be pulled and run from docker hub:

```shell
docker run --rm -p 5000:5000 --name mi-code-challenge fremmen/mi-code-challenge:latest
```

The docker image is based on `python:3.8` and is 1.64GB in size. This is too large and a focus can be put on reducing the size. However, this is not the focus of the project and therefore it was ignored.

## Test definitions

### Sanity checks

The objective states that any of the simulations are within the boundaries of Berlin.
A sanity check is made in the visualiser to visually confirm that the bbox is within bounds.
Addionally, this sanity check should be provoked in the Simulator class to mathematically verify the solutions integrity.
However modifying the Simulator class was out of scope.

## Points of improvement

### Web app

- I replaced the React app with a Flask app. Flask is not good for production environments.
- As can be observed in `webapp/routes.py`, HTTPS is forced before each request. The flask app can be extended using such functionalities.
- No caching is used.

### Static Data

- The static data is re-read on every simulation. Both simulator and visualiser class re-read the data.
This is ofcourse not necessary.

### Visualisations

- The visualisations are generated to a directory, and this directory is cleaned up before a new request is completed.
This is ok, but it would be better to generate it on-the-fly.

- The Google Maps web page displays an error "This page can't load Google Maps correctly." due to no API key being present for this project.

### Other

- The Simulator requires a GeoPandas version of 0.5.0. In this version a FutureWarning is given for the initialisation of a GeoDataFrame with coordinate systems. This is according to [this stackexchange post](https://gis.stackexchange.com/questions/348997/constant-future-warnings-with-new-pyproj) fixed in version > 0.7.0. However, touching the requirements for the simulator is out of scope. Fixing the warnings will be done after the migration to > 0.7.0 is done.
- The Visualiser class is quite slow due to queries to the web tile servers. This can be improved using cached tiles.
