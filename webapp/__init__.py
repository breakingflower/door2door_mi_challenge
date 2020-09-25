from flask import Flask
from flask_wtf import CSRFProtect

from webapp.routes import routes
from webapp.config import Config

from utilities.staticdatareader import StaticDataReader

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