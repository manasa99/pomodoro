from flask import request, jsonify, render_template, Blueprint
from app.models.models import TimerData, Record, UserData
from app import app, db

timer_bp = Blueprint("timer", __name__,template_folder="templates", url_prefix="/timerbp")

"""
TimerData endpoints
Get -> Get TimerData for a specific id given timer_id or all the timers present
Post -> Post a new Timer to the TimerData
Put -> Update an existing timer with the given timer_id
Delete -> Delete an existing timer with the given timer_id
"""
@timer_bp.route('/', methods=['GET'])
def get_timer_data():
    timer_id = request.args.get('timer_id')
    if timer_id:
        timer = TimerData.query.filter_by(id=timer_id).first()
        if timer:
            return jsonify({'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id}), 200
        return jsonify({'message': 'Timer not found'}), 404
    else:
        timers = TimerData.query.all()
        if not timers:
            return jsonify({"message": "No Timers"}), 200
        return jsonify([{'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id} for timer in timers]), 200


@timer_bp.route('/', methods=['POST'])
def post_timer_data():
    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    time = data.get('time')
    user_id = data.get('user_id', None)
    global_timer = user_id is None

    if not name or time is None:
        return jsonify({'message': 'Missing name or time'}), 400

    new_timer = TimerData(name=name, time=time, isGlobal=global_timer, user_id=user_id)

    db.session.add(new_timer)
    db.session.commit()

    return jsonify({'message': 'Timer created successfully', 'id': str(new_timer.id)}), 201

@timer_bp.route('/<timer_id>', methods=['PUT'])
def update_timer_data(timer_id):
    timer = TimerData.query.filter_by(id=timer_id).first()
    if not timer:
        return jsonify({'message': 'Timer not found'}), 404

    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    time = data.get('time')
    user_id = data.get('user_id', None)
    global_timer = user_id is None

    if not name or time is None:
        return jsonify({'message': 'Missing name or time'}), 400

    timer.name = name
    timer.time = time
    timer.isGlobal = global_timer
    timer.user_id = user_id

    db.session.commit()

    return jsonify({'message': 'Timer updated successfully'}), 200

@timer_bp.route('/<timer_id>', methods=['DELETE'])
def delete_timer_data(timer_id):
    timer = TimerData.query.filter_by(id=timer_id).first()
    if not timer:
        return jsonify({'message': 'Timer not found'}), 404

    db.session.delete(timer)
    db.session.commit()
    return jsonify({'message': 'Timer deleted successfully'}), 200


