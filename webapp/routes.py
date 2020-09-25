
from flask import (Flask, render_template, request, 
                    redirect, url_for, Blueprint)

from webapp.forms import TriggerForm

from simulator.simulator import Simulator
from visualiser.visualiser import Visualiser

routes = Blueprint('routes', __name__)

@routes.before_request
def before_request():
    """
    Forwards http to https (showcase)
    """
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@routes.route('/visualise')
def visualise():
    """
    Renders a page with the image located in /webapp/static/plot.png.
    The image is made prior to this route, therefore it will be the last generated
    simulation.
    """
    return render_template('visualise.html', image_url='/webapp/static/plot.png')

@routes.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the home page. This page contains an instance of a TriggerForm.
    The TriggerForm contains input fields for the simulation. If the submit
    button is pressed, a simulation is triggered and the results are visualised
    using the Simulator and Visualiser class.
    """
    form = TriggerForm() 

    if form.validate_on_submit(): 

        # number of requests
        number_of_requests = form.number_of_requests_field.data

        # the bounding box is a string, convert it to a tuple
        bounding_box = (form.x1_field.data, form.y1_field.data, 
                        form.x2_field.data, form.y2_field.data)

        # simulator instance creation
        simulation_result = Simulator(bounding_box).simulate(number_of_requests)

        # generate a figure
        Visualiser().generate_figure(simulation_result)
        
        # redirect to the visualise endpoint
        return redirect(url_for('routes.visualise'))

    return render_template('home.html', title="MI Code Challenge", form=form)
