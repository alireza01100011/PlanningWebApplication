from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, SelectField, DateField

from utlis.forms import _get_fields, MultiCheckboxField


class TaskForm(FlaskForm):
    title = StringField(description='Add Title :',
                        validators=(DataRequired(), Length(1, 128)))
    
    description = TextAreaField(description='Add Description',
                                validators=(Length(1, 2048),))
    
    group = SelectField(label='Select The Task Group')

    deadline = DateField(description='Deadline Time',
            format='%Y-%m-%d', validators=(DataRequired(),))
    
    #  [(1, 5)]+[(, reminder_t) for reminder_t in range(15, 61, 15)]
    # def _list_choices()->list[tuple[int, int]]:
    #     count, choices = 2, [2, '5']
    #     for reminder_t in range(15, 61, 15):
    #         count += 1
    #         choices.append((count, f'{reminder_t}'))
    #     return choices
    # reminder = MultiCheckboxField(label='Reminder', description='Reminder Before The Event') 

    def get_fields(self):
        return _get_fields(self)