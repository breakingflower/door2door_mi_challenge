###################################################################
# Script Name	 : "CLEANUP.PY"                                                                                         
# Description	 : Class definition for Cleaner                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

import os
import glob

class Cleaner:
    """
    Class to clean up the application directory
    """

    @staticmethod
    def remove_previous_simulation_results(static_path: str): 
        """
        Removes all files with the .png and .html extension from the static folder
        """

        previous_simulation_images = glob.glob(f'{static_path}/*.png')
        previous_simulation_html = glob.glob(f'{static_path}/*.html')

        for f in previous_simulation_images: 
            os.remove(f) 
        
        for f in previous_simulation_html: 
            os.remove(f) 



        
