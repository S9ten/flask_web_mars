import datetime
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('users.id'))  # id руководителя,

    job = sqlalchemy.Column(sqlalchemy.String)  # description описание работы
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # hours объем работы в часах
    collaborators = sqlalchemy.Column(sqlalchemy.String)  # список id участников
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now())  # дата начала

    end_date = sqlalchemy.Column(sqlalchemy.DateTime)  # дата окончания

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)  # признак завершения

    user = orm.relationship('User')