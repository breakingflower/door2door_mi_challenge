###################################################################
# Script Name	 : "VISUALISER.PY"                                                                                         
# Description	 : Visualiser class for mi-code-challenge                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

class Visualiser: 

    def __init__(self):
        pass

    def __repr__(self): 
        return "Visualiser class for mi-code-challenge"

    def generate_figure(self, simulation_results: dict): 
        """
        Visualises the results given in the simulation dictionary
        :type simulation_results: dict
        :rtype 
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

        # f, ax = plt.figure() 

        simulation_results['most_popular_dropoff_points'].plot() 

        plt.savefig('webapp/static/plot.png')
