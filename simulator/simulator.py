import geopandas as gpd
from shapely.geometry import box

class Simulator:
    booking_distance_distribution = [0.2, 0.1, 0.3, 0.4]
    max_popular_points = 10
    
    def __init__(self, bounding_box: tuple, path_to_stops='data/berlin_stops.geojson'):
        self.bounding_box = bounding_box
        self.path_to_stops = path_to_stops

    def simulate(self, number_of_requests: int) -> dict:
        booking_distance_bins = self.get_booking_distance_bins(
            number_of_requests)
        number_of_sample_points = min(
            number_of_requests, self.max_popular_points)
        most_popular_dropoff_points = self.get_random_points(
            number_of_sample_points)
        most_popular_pickup_points = self.get_random_points(
            number_of_sample_points)
            
        return {
            'booking_distance_bins': booking_distance_bins,
            'most_popular_dropoff_points': most_popular_dropoff_points,
            'most_popular_pickup_points': most_popular_pickup_points
        }

    def get_booking_distance_bins(self, number_of_requests: int) -> dict:
        return {
            f'From {i}->{i+1}km': round(number_of_requests * x)
            for i, x in enumerate(self.booking_distance_distribution)}

    def get_random_points(self, n: int) -> gpd.GeoDataFrame:
        bounding_box_shape = box(*self.bounding_box)
        geodataframe = gpd.read_file(self.path_to_stops, crs='epsg:4326')
        within_bounds = geodataframe[geodataframe.within(bounding_box_shape)]

        # if less than n points are available, return the ones that are available.
        if len(within_bounds) < n: 
            return within_bounds

        return within_bounds.sample(n) # .to_json()
