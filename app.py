###################################################################
# Script Name	 : "APP.PY"                                                                                         
# Description	 : Main file for the mi-code-challenge                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

from simulator.simulator import Simulator
from visualiser.visualiser import Visualiser

if __name__ == "__main__":
    
    # bounding_box = (min_longitude, min_latitude, max_longitude, max_latitude)
    bounding_box = (13.34014892578125, 52.52791908000258, 
                    13.506317138671875, 52.562995039558004)

    # number_of_requests is the number of requests to our Ridepooling service to "simulate".
    number_of_requests = 6

    # The bounding box should be inside berlin
    # https://www.openstreetmap.org/relation/62422#map=10/52.4556/13.7755
    


    # get the result using the simulator
    result = Simulator(bounding_box).simulate(number_of_requests)

    # visualise the results using the visualiser
    Visualiser().visualise(simulation_results=result)
    
