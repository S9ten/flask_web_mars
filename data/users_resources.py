from datetime import datetime

from flask import jsonify
from flask_restful import Resource, reqparse, abort
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password')
parser.add_argument('modified_date', type=datetime)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        from data import db_session
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'users': users.to_dict(
            rules=('-jobs.user', '-departments.user'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            rules=('-jobs', 'departments.user')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            password=args['password'],
            modified_date=args['modified_date']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        abort(404, message=f"Users {users_id} not found")
