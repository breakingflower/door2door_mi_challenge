import os
import glob

from flask import current_app

class Cleaner:
    """
    Class to clean up the results of the simulation / visualisation
    """

    @staticmethod
    def remove_previous_simulation_results(): 
        """
        Removes all files with the .png and .html extension from the static folder
        """

        static_path = os.path.join(current_app.root_path, current_app.static_folder)
        
        previous_simulation_images = glob.glob(f'{static_path}/*.png')
        previous_simulation_html = glob.glob(f'{static_path}/*.html')

        for f in previous_simulation_images: 
            os.remove(f) 
        
        for f in previous_simulation_html: 
            os.remove(f) 



        