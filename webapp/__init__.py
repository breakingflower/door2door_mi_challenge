from flask import Flask
from flask_wtf import CSRFProtect

from webapp.routes import routes
from utilities.staticdatareader import StaticDataReader


def create_app():
    """
    Creates a basic Flask application. 
    Uses CSRF and registers the routing blueprints.
    
    :rtype flask.app.Flask
    """

    # create a Flask application
    application =  Flask(__name__, static_url_path='/static', 
                            static_folder='static',
                            template_folder='templates')

    # CSRF is required for submitting forms (e.g. to run a simulation)
    application.config['SECRET_KEY'] = "MI_CODE_CHALLENGE_FLORIS"
    csrf = CSRFProtect()
    csrf.init_app(application)

    # register the routing blueprint
    application.register_blueprint(routes)

    return application