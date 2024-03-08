from flask import request, jsonify, views, Blueprint
from app import db, app
from app.models.models import TimerData
from app.forms.forms import TimerForm

class TimerDataAPI(views.MethodView):
    def get(self, timer_id=None):
        timer_id = request.args.get('timer_id')
        if timer_id:
            timer = TimerData.query.filter_by(id=timer_id).first()
            if timer:
                return jsonify(
                    {'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id}), 200
            return jsonify({'message': 'Timer not found'}), 404
        else:
            timers = TimerData.query.all()
            if not timers:
                return jsonify({"message": "No Timers"}), 200
            return jsonify(
                [{'name': timer.name, 'time': timer.time, 'isGlobal': timer.isGlobal, 'user_id': timer.user_id} for
                 timer in timers]), 200

    def post(self):
        form = TimerForm()
        if form.validate_on_submit():
            name = form.name.data
            time = form.time.data
            global_timer = form.global_timer.data
            new_timer = TimerData(name=name, time=time, isGlobal=global_timer)
            db.session.add(new_timer)
            db.session.commit()
            return jsonify({'message': 'Timer created successfully', 'id': str(new_timer.id)}), 201
        return jsonify({'message': 'Invalid form data'}), 400


    # def post(self):
    #     data = request.json
    #     if not data:
    #         return jsonify({'message': 'No input data provided'}), 400
    #
    #     name = data.get('name')
    #     time = data.get('time')
    #     user_id = data.get('user_id', None)
    #     global_timer = user_id is None
    #     if not name or time is None:
    #         return jsonify({'message': 'Missing name or time'}), 400
    #
    #     new_timer = TimerData(name=name, time=time, isGlobal=global_timer, user_id=user_id)
    #
    #     db.session.add(new_timer)
    #     db.session.commit()
    #     return jsonify({'message': 'Timer created successfully', 'id': str(new_timer.id)}), 201

    def put(self, timer_id):
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

    def delete(self, timer_id):
        timer = TimerData.query.filter_by(id=timer_id).first()
        if not timer:
            return jsonify({'message': 'Timer not found'}), 404
        db.session.delete(timer)
        db.session.commit()
        return jsonify({'message': 'Timer deleted successfully'}), 200


# timer_blueprint = Blueprint('timerview', __name__, url_prefix="/timerviewbp")
#
# # Register the view
# timer_view = TimerDataAPI.as_view('timer_api')
# timer_blueprint.add_url_rule('/', view_func=timer_view, methods=['GET', 'POST'])
# timer_blueprint.add_url_rule('/<int:timer_id>', view_func=timer_view, methods=['GET', 'PUT', 'DELETE'])
