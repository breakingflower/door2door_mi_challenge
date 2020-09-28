###################################################################
# Script Name	 : "VISUALISER.PY"                                                                                         
# Description	 : Visualiser class for mi-code-challenge                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

# To ignore future warnings w.r.t. geopandas 0.5.0 
# TODO: Remove this when migrating to geopandas > 0.7.0 !
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# data manipulation
import pandas as pd
import geopandas as gpd

# for hints
from utilities.bounding_box import BoundingBox
from utilities.staticdatareader import StaticDataReader

# plotting figures
import matplotlib
matplotlib.use('Agg') # non interactive backend for matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Polygon # to plot berlin bounds as polygon

# for visualiser ID generation
from random import randint

# google maps plotting
import gmplot

# to edit the contextily cache directory
import os

class Visualiser: 
    """
    Class to generate visualisations based on the output of a Simulator instance.
    """

    ## TODO: Use booking bins

    def __init__(self, bounding_box: BoundingBox, simulation_results: dict, static_data: StaticDataReader, static_path: str):
        
        # read the static data files. 
        self.static_data = static_data

        # set the simulation results
        self.bounding_box = bounding_box
        self.simulation_results = simulation_results

        # a random identifier for the simulation
        self.id = randint(0, 69420)
        
        # the directory to store the output visualisations
        self.static_path = static_path

        # set the contextily cache dir to reduce downloads
        ctx.set_cache_dir(os.path.join(os.getcwd(), 'data', 'contextily_cache'))

        # set the visualiser coordinate system. Usually web tiles are provided using web mercator
        self.crs_epsg = 3857

    def __repr__(self): 
        return f"Visualiser class for mi-code-challenge around {self.bounding_box.center}."

    def generate_overview_figure(self):
        """
        Generates an overview image using matplotlib.
        The data is first converted to the correct Coordinate system. 
        The following features can be observed in the output image: 
        - all of the berlin stops
        - a visual sanity check containing the bounds of berlin, 
            to assert that the bounding box is not outside of berlin
        - the bounding box itself
        - the simulation results: pickups / dropoffs
        - a background map using contextily / openstreetmap data
        The image is saved in the webapp/static directory with the identifier of the Visualiser instance.
        """

        _, ax = plt.subplots(figsize=(15,12)) 
        plt.title('Overview plot')

        # plotting all of the stops in Berlin in correct crs
        if not self.static_data.berlin_stops.empty:
            self.static_data.berlin_stops.to_crs(epsg=self.crs_epsg).plot(ax=ax, marker='.', markersize=15, label='Stops') 
        
        # plotting the polygon around berlin
        if not self.static_data.berlin_bounds.empty:
            # convert the bounds of berlin to the correct crs
            berlin_bounds_points = self.static_data.berlin_bounds.to_crs(epsg=self.crs_epsg)
            # convert the points to a polygon
            berlin_bounds_poly = Polygon([[p.x, p.y] for p in berlin_bounds_points.geometry])
            # plot the polygon's exterior --> this is the bounds of berlin.
            ax.plot(*berlin_bounds_poly.exterior.xy, color='red')

        # plot the bounding box as a matplotlib Rectangle
        x1, y1, x2, y2 = self.bounding_box.to_crs(epsg=self.crs_epsg)
        bounding_box_handle = matplotlib.patches.Rectangle(
            xy=(min(x1,x2), min(y1,y2)), 
            width=abs(x2-x1), 
            height=abs(y2-y1), 
            fill=False,
            color='red',
            linewidth=3,
            label='bbox'
        )
        ax.add_patch(bounding_box_handle)

        # Set the coordinate system of the simulation to EPSG 3857. This is the most popular one for web tiles
        pickup_data = self.simulation_results['most_popular_pickup_points'].to_crs(epsg=self.crs_epsg)
        dropoff_data = self.simulation_results['most_popular_dropoff_points'].to_crs(epsg=self.crs_epsg)
        # plot pickup points
        pickup_data.plot(ax=ax, 
                        marker='^',          
                        markersize=150, 
                        color='green', 
                        label='Pickup Requests')
        # plot dropoff points
        dropoff_data.plot(ax=ax, 
                        marker='v', 
                        markersize=150, 
                        color='red', 
                        label='Dropoff Requests')
        # set labels on axes
        ax.set(xlabel="Latitude", ylabel="Longitude")
        # add a basemap using contextily
        ctx.add_basemap(ax)
        # remove axes
        ax.set_axis_off()
        # legend to the right of the figure
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        # save the figure
        plt.savefig(f'{self.static_path}/{self.id}_overview_plot.png')
        # close the image
        plt.close()

    def generate_closeup_figure(self): 
        """
        Generates a closeup image using matplotlib.
        The data is first converted to the correct Coordinate system. 
        Visualises the results provided by the simulation with the following features: 
        - the bounding box itself
        - the simulation results: pickups / dropoffs
        The image is saved in the webapp/static directory with the identifier of the Visualiser instance.
        """

        _, ax = plt.subplots(figsize=(15,7)) 

        plt.title('Close up')
        # Set the coordinate system to EPSG 3857. This is the most popular CRS for web tiles
        pickup_data = self.simulation_results['most_popular_pickup_points'].to_crs(epsg=self.crs_epsg)
        dropoff_data = self.simulation_results['most_popular_dropoff_points'].to_crs(epsg=self.crs_epsg)
        # plot pickup points
        pickup_data.plot(ax=ax, 
                        marker='^',          
                        markersize=150, 
                        color='green', 
                        label='Pickup Requests')
        # plot dropoff points
        dropoff_data.plot(ax=ax, 
                        marker='v', 
                        markersize=150, 
                        color='red', 
                        label='Dropoff Requests')
        # set labels on axes
        ax.set(xlabel="Latitude", ylabel="Longitude")
        # add a basemap using contextily & remove axes
        ctx.add_basemap(ax=ax)
        ax.set_axis_off() 
        # legend to the right of the figure
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        # save figure
        plt.savefig(f'{self.static_path}/{self.id}_closeup_plot.png')
        # close 
        plt.close()

    def generate_gmap(self): 
        """
        Generates an interactive google maps plot as an HTML file using gmplot.
        No API key was defined, so only for development purposes.
        """
        # Create the map plotter. No API key for this project
        apikey = ''
        gmap = gmplot.GoogleMapPlotter(*self.bounding_box.center, 13, apikey=apikey, map_type='hybrid')
        
        # scatter pickup points
        gmap.scatter(self.simulation_results['most_popular_pickup_points'].geometry.y, 
                        self.simulation_results['most_popular_pickup_points'].geometry.x, 
                        color='green', marker=True)
        # add the identifier to the marker. Unfortunately no function for gmap.scatter to annotate
        for _, row in self.simulation_results['most_popular_pickup_points'].iterrows(): 
            gmap.text(row.geometry.y, row.geometry.x, row.id)
    
        # scatter dropoff points
        gmap.scatter(self.simulation_results['most_popular_dropoff_points'].geometry.y, 
                        self.simulation_results['most_popular_dropoff_points'].geometry.x, 
                        color='red', marker=True)
        # add the identifier to the marker. Unfortunately no function for gmap.scatter to annotate
        for _, row in self.simulation_results['most_popular_dropoff_points'].iterrows(): 
            gmap.text(row.geometry.y, row.geometry.x, row.id)
            
        # plot bounding box. The function requires four coordinates for a box.
        gmap.polygon(
            self.bounding_box.lats,
            self.bounding_box.lons,
            color='orange', 
            edge_width=5
        )
    
        # Draw the map to an HTML file:
        gmap.draw(f'{self.static_path}/{self.id}_map.html')
