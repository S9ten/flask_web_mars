import flask
from flask import jsonify, request
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    rules=('-user.jobs', '-team_leader.jobs', '-user.departments', '-user.'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict(rules=(
                '-user.jobs', '-team_leader.jobs', '-user.departments', '-team_leader.departments'))
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(team_leader=request.json['team_leader'],
                job=request.json['job'],
                work_size=request.json['work_size'])
    if 'id' in request.json:
        if db_sess.query(Jobs).get(request.json('id')):
            return jsonify({'error': 'id_already_exist'})
        jobs.id = request.json('id')
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']
    if 'start_date' in request.json:
        jobs.start_date = request.json['start_date']
    if 'end_date' in request.json:
        jobs.end_date = request.json['end_date']
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/job/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})

    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'start_date' in request.json:
        job.start_date = request.json['start_date']
    if 'end_date' in request.json:
        job.end_date = request.json['end_date']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})