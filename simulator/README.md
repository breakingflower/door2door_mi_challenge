# Mock-Simulator

This module (`simulator.py`) provides a class `Simulator` that returns some mock simulation results. It does not actually simulate any services, etc, but it should be used as if it did.

## Setup
1. Initialize a virtual environment and install the requirements in `requirements.txt`.
2. Adjust `Simulator.path_to_stops` based on the final architecture of the project/where it will be run from.

## Usage
- Create a `Simulator` instance (`Simulator(bounding_box)`) where `bounding_box` is a `tuple` that looks like this:
```python
# bounding_box = (min_longitude, min_latitude, max_longitude, max_latitude)
bounding_box = (13.34014892578125, 52.52791908000258, 13.506317138671875, 52.562995039558004)
```
The bounding box has to be in Berlin.

- Get the simulation results:
```python
result = Simulator(bounding_box).simulate(number_of_requests)
```
where `number_of_requests` is the number of requests to our Ridepooling service to "simulate".

## Output
The `result` we get is a `dict` that looks like the following:

| Key                           | Type                                                               | Description                                                                                                                     |
|-------------------------------|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `booking_distance_bins`       | dict                                                               | How many bookings happened for every "kilometer bin". E.g. how many bookings had a distance between 0 and 1km, 1 and 2kms, etc. |
| `most_popular_dropoff_points` | String (valid [`.geojson`](https://en.wikipedia.org/wiki/GeoJSON)) | Which points within the simulated bounding box were the most popular dropoff points.                                            |
| `most_popular_pickup_points`  | String (valid [`.geojson`](https://en.wikipedia.org/wiki/GeoJSON)) | Which points within the simulated bounding box were the most popular pickup points.                                             |
