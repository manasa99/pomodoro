from flask import request, jsonify, render_template, Blueprint
from app.models.models import TimerData, Record, UserData
from app import app, db


"""
Basic Response using render_template. Find the hello.html in templates folder.
If a name is given it returns Hello, <name> else Hello, <world>"
"""

def hello(name=None):
    if name==None or name=="":
        return render_template("hello.html")
    return render_template("hello.html", name=name)

"""
Use this to see which method is being called
"""
@app.route('/meth', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_the_method_called():
    if request.method == 'GET':
        return 'This is a GET request'
    elif request.method == 'POST':
        return 'This is a POST request'
    elif request.method == 'PUT':
        return 'This is a PUT request'
    elif request.method == 'DELETE':
        return 'This is a DELETE request'
    else:
        return 'Unsupported HTTP method'

"""
TimerData endpoints
Get -> Get TimerData for a specific id given timer_id or all the timers present
Post -> Post a new Timer to the TimerData
Put -> Update an existing timer with the given timer_id
Delete -> Delete an existing timer with the given timer_id
"""
# @app.route('/timerdata', methods=['GET'])
# def get_timer_data():
#     timer_id = request.args.get('timer_id')
#     if timer_id:
#         timer = TimerData.query.filter_by(id=timer_id).first()
#         if timer:
#             return jsonify({'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id}), 200
#         return jsonify({'message': 'Timer not found'}), 404
#     else:
#         timers = TimerData.query.all()
#         if not timers:
#             return jsonify({"message": "No Timers"}), 200
#         return jsonify([{'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id} for timer in timers]), 200
#
#
# @app.route('/timerdata', methods=['POST'])
# def post_timer_data():
#     data = request.json
#     if not data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     name = data.get('name')
#     time = data.get('time')
#     user_id = data.get('user_id', None)
#     global_timer = user_id is None
#
#     if not name or time is None:
#         return jsonify({'message': 'Missing name or time'}), 400
#
#     new_timer = TimerData(name=name, time=time, isGlobal=global_timer, user_id=user_id)
#
#     db.session.add(new_timer)
#     db.session.commit()
#
#     return jsonify({'message': 'Timer created successfully', 'id': str(new_timer.id)}), 201
#
# @app.route('/timerdata/<timer_id>', methods=['PUT'])
# def update_timer_data(timer_id):
#     timer = TimerData.query.filter_by(id=timer_id).first()
#     if not timer:
#         return jsonify({'message': 'Timer not found'}), 404
#
#     data = request.json
#     if not data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     name = data.get('name')
#     time = data.get('time')
#     user_id = data.get('user_id', None)
#     global_timer = user_id is None
#
#     if not name or time is None:
#         return jsonify({'message': 'Missing name or time'}), 400
#
#     timer.name = name
#     timer.time = time
#     timer.isGlobal = global_timer
#     timer.user_id = user_id
#
#     db.session.commit()
#
#     return jsonify({'message': 'Timer updated successfully'}), 200
#
# @app.route('/timerdata/<timer_id>', methods=['DELETE'])
# def delete_timer_data(timer_id):
#     timer = TimerData.query.filter_by(id=timer_id).first()
#     if not timer:
#         return jsonify({'message': 'Timer not found'}), 404
#
#     db.session.delete(timer)
#     db.session.commit()
#     return jsonify({'message': 'Timer deleted successfully'}), 200


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


@app.route('/calculate/<int:a>/<int:b>')
def addition(a, b):
    return str(a+b)

@app.route("/calc")
def addition1():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return str(a+b)
