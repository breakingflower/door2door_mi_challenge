
from flask import (Flask, render_template, request, 
                    redirect, url_for, Blueprint)

from webapp.forms import TriggerForm

from simulator.simulator import Simulator
from visualiser.visualiser import Visualiser

import random 

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

@routes.route('/visualise/<int:viz_id>')
def visualise(viz_id):
    """
    Renders a page with generated images.
    The image is made prior to this route, and an ID is prepended to the filename.
    The id is passed as a parameter.
    :type viz_id: int
    """

    return render_template('visualise.html',
            overview_image_url= url_for('static', filename=f'{viz_id}_overview_plot.png'), 
            closeup_image_url=url_for('static', filename=f'{viz_id}_closeup_plot.png'),
            gmap_url=url_for('static', filename=f'{viz_id}_map.html'))

@routes.route('/', methods=['GET', 'POST'])
def trigger_page():
    """
    Renders the trigger page. This page contains an instance of a TriggerForm.
    The TriggerForm contains input fields for the simulation. If the submit
    button is pressed, a simulation is triggered and the results are visualised
    using the Visualiser class.
    """
    form = TriggerForm() 

    if form.validate_on_submit(): 

        # number of requests
        number_of_requests = form.number_of_requests_field.data

        # the bounding box is a string, convert it to a tuple
        bounding_box = (form.x1_field.data, form.y1_field.data, 
                        form.x2_field.data, form.y2_field.data)

        # simulator instance creation
        simulation_results = Simulator(bounding_box).simulate(number_of_requests)

        # generate a static figure
        viz = Visualiser(bounding_box, simulation_results)
        viz.generate_overview_figure()
        viz.generate_closeup_figure()
        viz.generate_gmap()
        
        # redirect to the visualise endpoint
        return redirect(url_for('routes.visualise', viz_id = viz.id))

    return render_template('home.html', title="MI Code Challenge", form=form)
