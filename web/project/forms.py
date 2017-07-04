from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Optional
import bson

def object_id_validator(form, field):
    if not bson.objectid.ObjectId.is_valid(field.data):
        raise ValidationError("Field must be a valid hex objectid")

class LoginForm(FlaskForm):
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class TodoForm(FlaskForm):
    object_id = HiddenField('object_id', validators=[Optional(), object_id_validator])
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
