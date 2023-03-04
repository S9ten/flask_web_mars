from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField, \
    DateTimeLocalField
from wtforms.validators import DataRequired, Optional


class JobForm(FlaskForm):
    team_leader = SelectField('Руководитель', coerce=int, validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborators = StringField('Список id участников', validators=[DataRequired()])
    start_date = DateTimeLocalField('Дата начала', format="%Y-%m-%dT%H:%M", validators=[Optional()])
    end_date = DateTimeLocalField('Дата окончания', format="%Y-%m-%dT%H:%M", validators=[Optional()])
    is_finished = BooleanField('Окончена')
    submit = SubmitField('Добавить')