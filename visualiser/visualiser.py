###################################################################
# Script Name	 : "VISUALISER.PY"                                                                                         
# Description	 : Visualiser class for mi-code-challenge                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

# plotting figures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# data manipulation
import pandas as pd
import geopandas as gpd

# static data files reader
from utilities.staticdatareader import StaticDataReader
# for cleanup of previous simulation results
from utilities.cleanup import Cleaner

# for visualiser ID generation
from random import randint

# google maps plotting
import gmplot

# to access the API key
from flask import current_app



class Visualiser: 

    ## TODO: Use booking bins


    def __init__(self, bounding_box: tuple, simulation_results: dict):
        
        # cleanup before we continue
        Cleaner.remove_previous_simulation_results() 

        # read the static data files. 
        # TODO: update to only read once.
        self.static_data = StaticDataReader()
        self.bounding_box = bounding_box
        self.simulation_results = simulation_results

        # a random identifier for the simulation
        self.id = randint(0, 69420)

    def __repr__(self): 
        return "Visualiser class for mi-code-challenge"

    def generate_overview_figure(self):
        """
        Generates an overview image using matplotlib with the following features: 
        - all of the berlin stops
        - a sanity check containing the bounds of berlin, to assert that the bounding box is not outside of berlin
        - the bounding box itself
        - the simulation results: pickups / dropoffs
        The image is saved in the webapp/static directory with the identifier of the Visualiser instance.
        """

        _, ax = plt.subplots(figsize=(10,8)) 
        plt.title('Overview plot')
        # plotting all of the stops in Berlin
        self.static_data.berlin_stops.plot(ax=ax, marker='.', markersize=15, label='Stops') 
        # plotting the city boundaries
        self.static_data.berlin_bounds.plot(ax=ax, marker='.', markersize=15, label='Bounds', color='red')
        # bounding box 
        x1, y1, x2, y2 = self.bounding_box
        bounding_box_handle = Rectangle(
            xy=(min(x1,x2), min(y1,y2)), 
            width=abs(x2-x1), 
            height=abs(y2-y1), 
            fill=False,
            color='red',
            linewidth=3,
            label='bbox'
        )
        ax.add_patch(bounding_box_handle)
        # Pickup data
        self.simulation_results['most_popular_pickup_points'].\
                                plot(ax=ax, 
                                marker='.', 
                                markersize=15, 
                                color='green', 
                                label='Pickup Requests')
        # Dropoff data
        self.simulation_results['most_popular_dropoff_points'].\
                                plot(ax=ax, 
                                marker='.', 
                                markersize=15, 
                                color='orange', 
                                label='Dropoff Requests')
        # set labels on axes
        ax.set(xlabel="Latitude", ylabel="Longitude")
        # legend to the right of the figure
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        # save the figure
        plt.savefig(f'webapp/static/{self.id}_overview_plot.png')
        # close the image
        plt.close()

    def generate_closeup_figure(self): 
        """
        Visualises the results provided by the simulation with the following features: 
        - the bounding box itself
        - the simulation results: pickups / dropoffs
        The image is saved in the webapp/static directory with the identifier of the Visualiser instance.
        """

        # Sim results look like this 
        # {
        #     'booking_distance_bins': booking_distance_bins, 
        #           -->  get_booking_distance_bins
        #           --> {'From 0->1km': 1, 'From 1->2km': 1, 'From 2->3km': 2, 'From 3->4km': 2}
        #     'most_popular_dropoff_points': most_popular_dropoff_points,
        #           --> get_random_points
        #           --> geodataframe with (index, name, id, geom) 
        #     'most_popular_pickup_points': most_popular_pickup_points --> get_random_points
        #           --> get_random_points
        #           --> geodataframe with (index, name, id, geom) and size number_of_requests
        # }

        _, ax = plt.subplots() 

        plt.title('Close up')
        # plot pickup points
        self.simulation_results['most_popular_pickup_points'].\
                                plot(ax=ax, 
                                marker='.', 
                                markersize=15, 
                                color='orange', 
                                label='Pickup Requests')
        # plot dropoff points
        self.simulation_results['most_popular_dropoff_points'].\
                                plot(ax=ax, 
                                marker='.', 
                                markersize=15, 
                                color='green', 
                                label='Dropoff Requests')
        # set labels on axes
        ax.set(xlabel="Latitude", ylabel="Longitude")
        # legend to the right of the figure
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        # save figure
        plt.savefig(f'webapp/static/{self.id}_closeup_plot.png')
        # close 
        plt.close()
    
    def _get_box_center(self): 
        """
        Calculates the bounding box center by averaging the lat/lon coordinates.
        Returns a tuple with the center of the box.
        eg (y0 + y1) / 2 , (x0 + x1) / 2
        """
        return (self.bounding_box[1] + self.bounding_box[3]) / 2, (self.bounding_box[0] + self.bounding_box[2]) / 2

    def generate_gmap(self): 
        """
        Generates an interactive google maps plot.
        No API key was defined, so only for development purposes.
        """
        # Create the map plotter:
        apikey = ''
        # apikey = '' # no API key for this project.
        gmap = gmplot.GoogleMapPlotter(*self._get_box_center(), 13, apikey=apikey, map_type='hybrid')

        
        # scatter pickup points
        gmap.scatter(self.simulation_results['most_popular_pickup_points'].geometry.y, 
                        self.simulation_results['most_popular_pickup_points'].geometry.x, 
                        color='blue', marker=True)
        # add the identifier to the marker
        for _, row in self.simulation_results['most_popular_pickup_points'].iterrows(): 
            gmap.text(row.geometry.y, row.geometry.x, row.id)
    
        # scatter dropoff points
        gmap.scatter(self.simulation_results['most_popular_dropoff_points'].geometry.y, 
                        self.simulation_results['most_popular_dropoff_points'].geometry.x, 
                        color='red', marker=True)
        # add the identifier to the marker
        for _, row in self.simulation_results['most_popular_dropoff_points'].iterrows(): 
            gmap.text(row.geometry.y, row.geometry.x, row.id)
            
        # plot bounding box. The function requires four coordinates for a box.
        gmap.polygon(
            [self.bounding_box[1], self.bounding_box[3], self.bounding_box[3], self.bounding_box[1]], 
            [self.bounding_box[0], self.bounding_box[0], self.bounding_box[2], self.bounding_box[2]],  
            color='orange', edge_width=5
        )
    
        # Draw the map to an HTML file:
        gmap.draw(f'webapp/static/{self.id}_map.html')
