from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.validators import Email 
from wtforms.validators import EqualTo

class NewTaskViewModel(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    submit = SubmitField('Create Task')