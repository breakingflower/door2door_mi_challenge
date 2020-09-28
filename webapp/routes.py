###################################################################
# Script Name	 : "ROUTES.PY"                                                                                         
# Description	 : Endpoint routing scheme for the python flask
#                   application.                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

from flask import (Flask, render_template, request, 
                    redirect, url_for, Blueprint, current_app)

from webapp.forms import TriggerForm
from simulator.simulator import Simulator
from visualiser.visualiser import Visualiser
from utilities.cleanup import Cleaner
from utilities.staticdatareader import StaticDataReader
from utilities.bounding_box import BoundingBox

import os
import random 

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def trigger_page():
    """
    Renders the trigger page. This page contains an instance of a TriggerForm.
    The TriggerForm contains input fields for the simulation. If the submit
    button is pressed, a simulation is triggered and the results are generated
    using the Visualiser class. If all succeeds, forward to endpoint "visualise"
    """
    form = TriggerForm() 

    # if the form is valid and the submit button was pressed
    if form.validate_on_submit(): 
        
        # get the static path from the current application to store the visualisations
        static_path = os.path.join(current_app.root_path, current_app.static_folder)

        # clean up the previous simulation results
        Cleaner().remove_previous_simulation_results(static_path=static_path)

        # retrieve number of requests from the form
        number_of_requests = form.number_of_requests_field.data

        # Create an instance of the bounding box class, using the form data
        bounding_box = BoundingBox(
            (
            form.x1_field.data, 
            form.y1_field.data, 
            form.x2_field.data, 
            form.y2_field.data
            )
        )

        # Create an instance of the StaticDataReader class.
        static_data = StaticDataReader(
            berlin_bounds_file=current_app.config['BERLIN_BOUNDS_FILE'], 
            berlin_stops_file=current_app.config['BERLIN_STOPS_FILE']
        ) 

        # Create an instance of the Simulator class.
        simulator = Simulator(
            bounding_box = bounding_box.bounding_box, 
            path_to_stops=current_app.config['BERLIN_STOPS_FILE']
        )
        # Run a simulation
        simulation_results = simulator.simulate(number_of_requests)

        # Create an instance of the Visualiser class.
        visualiser = Visualiser(
            bounding_box = bounding_box, 
            simulation_results = simulation_results, 
            static_path = static_path,
            static_data = static_data
        )

        # Generate visualisations
        visualiser.generate_overview_figure()
        visualiser.generate_closeup_figure()
        visualiser.generate_gmap()
        
        # redirect to the visualise endpoint
        return redirect(url_for('routes.visualise', visualiser_id = visualiser.id))

    # render a template for the trigger page.
    return render_template('trigger_page.html', title="MI Code Challenge", form=form)

@routes.route('/visualise/<int:visualiser_id>')
def visualise(visualiser_id):
    """
    Renders a page with generated images.
    The image is made prior to this route, and an ID is prepended to the filename.
    The id is passed as a parameter.
    :type visualiser_id: int
    """

    return render_template('visualise.html',
            overview_image_url= url_for('static', filename=f'{visualiser_id}_overview_plot.png'), 
            closeup_image_url=url_for('static', filename=f'{visualiser_id}_closeup_plot.png'),
            gmap_url=url_for('static', filename=f'{visualiser_id}_map.html'))

@routes.before_request
def before_request():
    """
    Forwards http to https
    """
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
