###################################################################
# Script Name	 : "APP.PY"                                                                                         
# Description	 : Main file for the mi-code-challenge. Launches a
#                  Flask webserver that shows a single button to 
#                  trigger a simulation and visualise the results.                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

from webapp import create_app

# Create a Flask application
application = create_app() 

if __name__ == "__main__":

    # Run the flask application
    application.run(debug=True)  
