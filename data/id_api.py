import flask
from flask import jsonify, request
from data import db_session
from data.jobs import Jobs
blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)
@blueprint.route('/api/news', methods=['POST'])
def create_news():