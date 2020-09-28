###################################################################
# Script Name	 : "__INIT__.PY"                                                                                         
# Description	 : Initialises python flask app using the application
#                       factory standard.                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

from flask import Flask
from flask_wtf import CSRFProtect

from webapp.routes import routes
from webapp.config import Config

def create_app():
    """
    Creates a basic Flask application. 
    Uses CSRF and registers the routing blueprints.
    
    :rtype flask.app.Flask
    """

    # create a Flask application
    application =  Flask(__name__)
    application.config.from_object(Config)

    # CSRF is required for submitting forms (e.g. to run a simulation)
    csrf = CSRFProtect()
    csrf.init_app(application)

    # register the routing blueprint
    application.register_blueprint(routes)

    return application