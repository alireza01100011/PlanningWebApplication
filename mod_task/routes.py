from flask import (render_template, abort, request)

from .models import Task
from .forms import TaskForm
from mod_task import task
from utlis.flask_login import login_required

@task.route('/')
def home():
    return 'hello world'


@task.route('/calendar')
# @login_required('task.calendar')
def calendar():
    return render_template('app/calendar.html')


@task.route('/add-task', methods=['GET', 'POST'])
# @login_required('task.calendar')
def add_task():
    form = TaskForm()
    # def _list_choices()->list[tuple[int, int]]:
    #     count, choices = 1, [1, '5']
    #     for reminder_t in range(15, 61, 15):
    #         count += 1
    #         choices.append((count, f'{reminder_t}'))
    #     return choices
    # form.reminder.choices = _list_choices()
    # return f'{form.reminder.choices}'
    if request.method == 'PSOT':
        if not form.validate_on_submit():
            return render_template('app/forms.html', form=form,
                                title='Create New Task')
        pass

    return render_template('app/form.html', form=form,
                           title='Create New Task')