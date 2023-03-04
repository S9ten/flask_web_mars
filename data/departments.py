import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Department(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))  # шеф
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # члены
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)  # электронная почта
    user = orm.relationship('User')

    def __repr__(self):
        return f"""id:{self.id}, title:{self.title}, email:{self.email}"""
