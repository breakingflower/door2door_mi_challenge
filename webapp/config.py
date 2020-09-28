###################################################################
# Script Name	 : "CONFIG.PY"                                                                                         
# Description	 : Class definition for the Config of the flask app                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

class Config:
    """
    Configuration Class for the MI-Code-Challenge Flask app.
    """

    SECRET_KEY="MI_CODE_CHALLENGE_FLORIS"
    STATIC_URL_PATH='/static'
    STATIC_FOLDER="/webapp/static"
    TEMPLATE_FOLDER="/webapp/templates"

    BERLIN_BOUNDS_FILE = 'data/berlin_bounds.poly'
    BERLIN_STOPS_FILE = 'data/berlin_stops.geojson'
