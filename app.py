###################################################################
# Script Name	 : "APP.PY"                                                                                         
# Description	 : Main file for the mi-code-challenge. Launches a
#                  Flask webserver that shows a single button to 
#                  trigger a simulation and visualise the resutls.                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

from flask import Flask
from flask_wtf import CSRFProtect

from webapp.routes import routes

# create a flask application
application =  Flask(__name__, static_url_path='/static', static_folder='static')

# CSRF is required for submitting forms (e.g. to run a simulation)
application.config['SECRET_KEY'] = "MI_CODE_CHALLENGE_FLORIS"
csrf = CSRFProtect()
csrf.init_app(application)

# route blueprints
application.register_blueprint(routes)

if __name__ == "__main__":

    # run the flask application
    application.run(debug=True)  
