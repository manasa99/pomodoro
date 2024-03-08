from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class TimerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    time = IntegerField('Time', validators=[DataRequired()])
    global_timer = BooleanField('IsGlobal', validators=[DataRequired()])
    user_id = StringField('User Id')