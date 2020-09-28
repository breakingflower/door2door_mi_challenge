# MI Challenge

This repository describes my implementation of the coding challenge after a first interview at Door2door Berlin. The project should be cloned from github [here](https://github.com/fl0r1s/door2door_mi_challenge). 

# Structure

The project contains `utilities`, `visualiser`, `simulator`, `webapp` and `test` modules.

The `simulator` module is a clone of the simulator directory in the [github page](https://github.com/door2door-io/mi-code-challenge), with some changes as highlighted in the *Edits in simulator* paragraph. The `visualiser` module is used to generate locally-stored visualisations, and the `webapp` module shows the results in a web interface made in Flask. A `utilities` module is used to read the static data files. A `test` module contains some tests defined for the project.

The `data` directory contains two static data files. Addionally, this folder contains a `contextily_cache` directory to reduce the amount of requests to a tiling server.

# Edits in simulator

- `Simulator.path_to_stops` is moved to be an instance variable.
- Added `simulator/__init__.py` to allow loading of the simulator as a module.
- `simulator/requirements.txt` are moved to `requirements.txt` and updated to match `pandas==1.0.1` due to import errors on version 1.1.2
- Return type of simulator is not jsonified, e.g. `get_random_points` returns a geodataframe.
- Sets a default coordinate system in the generated geodataframe: EPSG:4326 (WGS84). This is necessary for getting map tiles from contextily, which operates in the current version in EPSG:3857 - Web mercator.

# Python environment

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

# Running the application using the webapp module

The webapp module contains the web interface.
All of the webpages are generated using the python `flask` module.

Two directories are created in the webapp module:

- a `templates` directory to store the visualisation templates used to generate HTML. In this directory I have created four files: `layout.html` containing the essential layout (bootstrap) + a code block which we extend in the other pages. `home.html` is the landing page for the application. It contains a form that can be used to trigger a simulation & visualisation. `visualisation.html` is the visualisation page that loads the three visualisations and shows a button to perform a new simulation. A helper jinja file is given in `_macros.jinja` to facilitate generation of form elements.
- a `static` directory to store the generated images / maps.

Some other files are present:

- an `__init__.py` file to instantiate the module. This file creates the python flask application according to the [application factory](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/) standard. This is mainly used to easily extend a webapp with new functionality.
- a `config.py` file containing the config of the web app. These are mostly paths and other configuration requirements. We use a csrf token to allow for form submission in the html page.
- a `forms.py` file containing the web form that is shown as a homepage when running the app. This form data can be altered by the user. A test is made to assert that the fields are of correct data type and filled.
- a `routes.py` file containing the required routing points for the webapp. In essence only two routes are necessary: a `trigger_page` route to initialize the simulation and generate the resulting images, and a `visualise` route to visualise  the newly made results.

## Webapp in virtualenv

The webapp can be run from the project root using the previously defined environment.

```shell
source env/bin/activate
python app.py
```

A webserver will start on `localhost:5000`.

## Webapp in Docker

A docker image can be pulled and run directly from docker hub:

```shell
docker run --rm -p 5000:5000 --name mi-code-challenge fremmen/mi-code-challenge:latest
```

This docker image can also be locally built (architecture = amd64) from the project root:

```shell
docker build -t mi-code-challenge .
```

The locally built image can then be run with

```shell
docker run --rm -p 5000:5000 --name mi-code-challenge mi-code-challenge
```

Port 5000 is forwarded from container to host. A webserver will start on `localhost:5000`.

The docker image is based on `python:3.8` and is 1.33GB in size. This is too large and a focus can be put on reducing the size. However, this is not the focus of the project and therefore it was ignored.

# Running the application using the API

The modules can all be used as python3 modules. An import is done using e.g.

```python
from visualiser.visualiser import Visualiser
```

## API in python3 using Jupyter notebook

A jupyter notebook is given `API-showcase-notebook.ipynb` that walks through the each of the modules in the application seperately. This file also contains documentation on each of the functions / classes.

To open this file the user should install jupyterlab:

```shell
pip install jupyterlab
```

Afterwards, the file can be shown using

```shell
jupyter notebook API-showcase-notebook.ipynb
```

# After this I assume you have succesfully run the application and did some preliminary result generation.

# Test definitions

## Sanity checks

The objective states that any of the simulations are within the boundaries of Berlin.
A sanity check is made in the visualiser to visually confirm that the bbox is within bounds.
Addionally, this sanity check should be provoked in the Simulator class to mathematically verify the solutions integrity.
However modifying the Simulator class was out of scope.

## Webapp

A form is generated in the web interface at route `home` forces the user to input

- `float` in the x1,y1,x2,y2 fields
- `int` in the number_of_requests field.

If this is not true, the form will yield an error in the corresponding line and the request will not be forwarded until the user uses the correct datatype.

## API

If a user is not using the webserver but instead the API, some checks are performed:

- In `StaticDataReader`: does the berlin_stops / berlin_bounds file exist? If it does not, return an empty geodataframe.
- in `Visualiser.generate_overview_figure()`: if the geodataframe is empty, ignore it.

Several tests have been defined in the `tests` module. More specifically for the `BoundingBox, Simulator, StaticDataReader and Visualiser` classes. Some of the test modules suppress Future and Deprication Warnings. The tests can be run as follows:

### Running a single test

```shell
python -m unittest tests/xxxx.py
```

### Running all of the tests

```shell
python -m unittest discover tests
```

# Points of improvement

## Web app

- I replaced the React app with a Flask app. Flask is not good for production environments.
- As can be observed in `webapp/routes.py`, HTTPS is forced before each request. The flask app can be extended using such functionalities.
- Fetching the `contextily` web tiles can be very slow. An initial effort is made to reduce the number of required requests to the web tile server by hardcoding a cache path in the `data/contextily_cache` directory. Other options are available.

## Static Data

- The static data is re-read on every simulation. Both simulator and visualiser class re-read the data.
This is ofcourse not necessary.

## Visualisations

- The visualisations are generated to a directory, and this directory is cleaned up before a new request is completed when the webapp is used.
This is ok, but it would be better to generate it on-the-fly. An option is to show a default Berlin visualisation and data can be highlighted by for example selection using mouse input.
- A good extension to the visualisation module would be to use the `simulator.get_booking_distance_bins()` method. However, this method is not related to the actual sampled points so it was ignored for this project.
- No path is shown between sets of points. This is related to dropoff-pickup relationships.
- The Google Maps web page displays an error "This page can't load Google Maps correctly." due to no API key being present for this project.

## Other

- The Simulator requires a GeoPandas version of 0.5.0. In this version a FutureWarning is given for the initialisation of a GeoDataFrame with coordinate systems. This is according to [this stackexchange post](https://gis.stackexchange.com/questions/348997/constant-future-warnings-with-new-pyproj) fixed in version > 0.7.0. However, touching the requirements for the simulator is out of scope. Fixing the warnings will be done after the migration to > 0.7.0 is done.
- The Visualiser class is quite slow due to queries to the web tile servers. This can be improved using cached tiles.
- All of the classes are built to be easily extensible / maintainable.

## Timing

All of the cells in the `API-showcase-notebook` are timed using the `%%timeit` and `%%prun` commands and the following conclusions can be drawn:

| Class            | Method                     | Timeit              |
|------------------|----------------------------|---------------------|
| StaticDataReader | Constructor                | 134ms +1.03ms       |
| Simulator        | get_random_points()        | 97.2 ms + 276micros |
| Simulator        | simulate()                 | 198 ms + 3.2ms      |
| Visualiser       | generate_overview_figure() | 2.17s + 8.0ms       |
| Visualiser       | generate_closeup_figure()  | 1.24s + 8.19ms      |
| Visualiser       | generate_gmap()            | 4.78ms + 121micros  |

Both matplotlib / contextily generated images are very slow, with a factor 500 slower when compared to the gmplot implementation.

This is likely due to the queries to the map tile servers which is inherently slow. When starting from no cached tiles, a single image generation can take up to 5.7 seconds. A simple solution was to add a caching directory.

After closer inspection it was observed that in the generation of the overview image around 750-850ms (36%) of execution time was due to image operations (opening, scaling, resampling, ...). Furthermore, the reprojection to a different coordinate system was also very slow ~340ms (15,5%). These operations can yield very large performance improvements if tackled properly.
