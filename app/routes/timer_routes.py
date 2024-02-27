from flask import request, jsonify
from app.models.models import TimerData, Record, UserData
from app import app, db


"""
TimerData endpoints
Get -> Get TimerData for a specific id or all the timers present
Post -> Post a new Timer to the TimerData
"""
@app.route('/timerdata', methods=['GET'])
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


@app.route('/timerdata', methods=['POST'])
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



"""
Record endpoints
Get -> Get Record for:  
            -> a specific id
            -> a specific user
            -> a specific timer
            -> all records
Post -> Post a new Record to the Record
"""


@app.route('/record', methods=['GET'])
def get_record_data():
    record_id = request.args.get('record_id')
    timer_id = request.args.get('timer_id')
    user_id = request.args.get('user_id')
    if record_id:
        record = Record.query.filter_by(id=record_id).first()
        if record:
            return jsonify(record.json_format()), 200
        else:
            return jsonify({"message" : "record not found"}), 400
    elif timer_id:
        records = Record.query.filter_by(timer_id=timer_id).all()
        if records:
            return jsonify([record.json_format() for record in records]), 200
        else:
            return jsonify({"message" : "records not found for the timer_id"}), 400
    elif user_id:
        records = Record.query.filter_by(user_id=user_id).all()
        if records:
            return jsonify([record.json_format() for record in records]), 200
        else:
            return jsonify({"message" : "records not found for the user_id"}), 400
    else:
        records = Record.query.all()
        return jsonify([record.json_format() for record in records]), 200


@app.route('/record', methods = ['POST'])
def post_record_data():
    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    timer_id = data.get('timer_id')
    user_id = data.get('user_id')

    if not timer_id or user_id is None:
        return jsonify({'message': 'Missing timer_id or user_id'}), 400

    new_record = Record(timer_id=timer_id, user_id=user_id)

    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': 'Record created successfully', 'id': str(new_record.id)}), 201

