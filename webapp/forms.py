from wtforms import SubmitField, IntegerField, FloatField
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired

class TriggerForm(FlaskForm): 
    """
    A form definition to trigger a simulation.
    """

    # Define the bounding box fields. All are float fields (no other dtype allowed). All fields required
    x1_field = FloatField("x1", default=13.34014892578125, validators=[DataRequired()])
    y1_field = FloatField("y1", default=52.5279190800025, validators=[DataRequired()])
    x2_field = FloatField("x2", default=13.506317138671875, validators=[DataRequired()])
    y2_field = FloatField("y2", default=52.562995039558004, validators=[DataRequired()])

    # Number of requests field. Integer field (no other dtype allowed). Required
    number_of_requests_field = IntegerField(
        "Number of Requests",
        default=6,
        validators=[DataRequired()]
    )

    # Submit field
    submit = SubmitField(
        "Trigger Simulator & Visualise Results"
    )