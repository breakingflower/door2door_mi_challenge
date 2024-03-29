###################################################################
# Script Name	 : "STATICDATAREADER.PY"                                                                                         
# Description	 : Class definition for the static data file reader                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

import pandas as pd 
import geopandas as gpd 

from os.path import isfile

class StaticDataReader: 
    """
    Reads the static data files
    """

    def __init__(self, berlin_bounds_file, berlin_stops_file): 

        # set filenames
        self.berlin_bounds_file = berlin_bounds_file
        self.berlin_stops_file  = berlin_stops_file

        # read files 
        self.berlin_stops   = self._read_berlin_stops()
        self.berlin_bounds  = self._read_berlin_bounds()
    
    def __repr__(self): 
        return f"Reads static data files {self.berlin_bounds_file} and {self.berlin_stops_file}"

    def _read_berlin_stops(self) -> gpd.GeoDataFrame: 
        """
        Reads berlin stops from a geojson file, with epsg 4326. 
        If the file does not exist, return an empty geodataframe.
        :rtype geopandas.GeoDataFrame
        """

        if not isfile(self.berlin_stops_file): 
            return gpd.GeoDataFrame()

        return gpd.read_file(self.berlin_stops_file, crs='epsg:4326')

    def _read_berlin_bounds(self) -> gpd.GeoDataFrame: 
        """
        Reads berlin bounds from a poly file and set epsg to 4326.
        If the file does not exist, return an empty geodataframe.
        :rtype geopandas.GeoDataFrame
        """
        if not isfile(self.berlin_bounds_file): 
            return gpd.GeoDataFrame()

        df = pd.read_csv(self.berlin_bounds_file, delim_whitespace=True, header=None)
        df.columns = ['lat', 'lon']

        # create a geodataframe
        gdf = gpd.GeoDataFrame(
            df,
            geometry = gpd.points_from_xy(df.lat, df.lon)
        )

        # drop the lat, lon columns as they are in the geometry column
        gdf.drop(['lat', 'lon'], axis=1, inplace=True)
        # set the coordinate system. This has to be done this way due to geopandas==0.5.0
        gdf.crs = {'init': 'epsg:4326'}

        return gdf