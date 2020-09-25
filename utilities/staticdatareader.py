import pandas as pd 
import geopandas as gpd 

from flask import current_app

class StaticDataReader: 
    """
    Reads the static data files
    """

    def __init__(self): 

        # filenames read from current application config
        self.berlin_bounds_file = current_app.config['BERLIN_BOUNDS_FILE']
        self.berlin_stops_file  = current_app.config['BERLIN_STOPS_FILE']
    
        # read files 
        self.berlin_stops = self._read_berlin_stops()
        self.berlin_bounds = self._read_berlin_bounds()
    
    def __repr__(self): 
        return "Reads static data files"

    def _read_berlin_stops(self): 
        """
        Reads berlin stops from a geojson file
        :rtype geopandas.GeoDataFrame
        """
        return gpd.read_file(self.berlin_stops_file)

    def _read_berlin_bounds(self): 
        """
        Reads berlin bounds from a poly file. 
        :rtype geopandas.GeoDataFrame
        """
        df = pd.read_csv(self.berlin_bounds_file, delim_whitespace=True, header=None)
        df.columns = ['lat', 'lon']

        return gpd.GeoDataFrame(geometry = gpd.points_from_xy(df.lat, df.lon))