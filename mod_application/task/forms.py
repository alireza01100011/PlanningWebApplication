from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, SelectField

from utlis.forms import _get_fields, MultiCheckboxField

from mod_user.user.forms import User


class TaskForm(FlaskForm):
    title = StringField(description='Add Title :',
                        validators=(DataRequired(), Length(1, 128)))
    
    description = TextAreaField(description='Add Description',
                                validators=(Length(1, 2048),))
    
    calendar = SelectField(label='Select The Calendar', choices=['Tasks'])

    _list_times = [
        f'{h}:{m}' for h in range(0,24)
          for m in range(0, 46, 15) ]

    start = SelectField(description='Start Time',
                        validators=(DataRequired(),), choices=_list_times)
    
    end = SelectField(description='End Time', choices=_list_times)
    
    #  [(1, 5)]+[(, reminder_t) for reminder_t in range(15, 61, 15)]
    def _list_choices()->list[tuple[int, int]]:
        count, choices = 2, [2, '5']
        for reminder_t in range(15, 61, 15):
            count += 1
            choices.append((count, f'{reminder_t}'))
        return choices
    reminder = MultiCheckboxField(description='Reminder Before The Event',
                                  coerce=int, choices=_list_choices()) 

    def get_fields(self):
        return _get_fields(self)