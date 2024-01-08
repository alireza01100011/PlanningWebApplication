from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, ColorField

from utlis.forms import _get_fields


class GroupForm(FlaskForm):
    title = StringField(description='Add Title',
                        validators=(DataRequired(), Length(1, 128)))
    
    description = TextAreaField(description='Add Description',
                                validators=(Length(1, 2048),))
    
    color = ColorField(label='Select Group Color')

    
    def get_fields(self):
        return _get_fields(self)