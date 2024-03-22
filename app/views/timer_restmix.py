from flask import jsonify, request, redirect, render_template, url_for, make_response
from flask_restx import Resource, Namespace, fields, Api
from app.models.models import TimerData
from werkzeug.datastructures import Headers
from app import app
from app.forms.forms import TimerForm

# Assuming CRUDMixin is defined somewhere above or in a separate module

# Create a namespace
timer_ns = Namespace('timerrestmix', description='Timer data operations')

# Create an Api object and add the namespace to it
api = Api(app, version='1.0', prefix='/api', title='Timer API', description='A simple Timer API')
api.add_namespace(timer_ns)

timer_model = api.model('TimerModel', {
    'name': fields.String(required=True, description='The timer name'),
    'time': fields.Integer(required=True, description='The timer duration in seconds'),
    'isGlobal': fields.Boolean(description='Indicates if the timer is global'),
    'user_id': fields.String(description='The ID of the user owning the timer')
})

@timer_ns.route('/')
class TimerList(Resource):
    @timer_ns.doc('list_timers')
    @timer_ns.marshal_list_with(timer_model)
    def get(self):
        """List all timers"""
        return TimerData.query.all()

    @timer_ns.doc('create_timer')
    @timer_ns.expect(timer_model)
    @timer_ns.marshal_with(timer_model, code=201)
    def post(self):
        """Create a new timer"""
        data = timer_ns.payload
        new_timer = TimerData().save(name=data['name'], time=data['time'], isGlobal=data['isGlobal'], user_id=data.get('user_id'))
        return new_timer, 201

@timer_ns.route('/<string:id>')
@timer_ns.response(404, 'Timer not found')
@timer_ns.param('id', 'The timer identifier')
class Timer(Resource):
    @timer_ns.doc('get_timer')
    @timer_ns.marshal_with(timer_model)
    def get(self, id):
        """Fetch a timer given its identifier"""
        timer = TimerData.get_by_id(id)
        if not timer:
            timer_ns.abort(404)
        return timer

    @timer_ns.expect(timer_model)
    @timer_ns.marshal_with(timer_model)
    def put(self, id):
        """Update a timer given its identifier"""
        timer = TimerData.get_by_id(id)
        if not timer:
            timer_ns.abort(404)
        data = timer_ns.payload
        timer.update(name=data['name'], time=data['time'], isGlobal=data['isGlobal'], user_id=data.get('user_id'))
        return timer

    @timer_ns.doc('delete_timer')
    @timer_ns.response(204, 'Timer deleted')
    def delete(self, id):
        """Delete a timer given its identifier"""
        timer = TimerData.get_by_id(id)
        if not timer:
            timer_ns.abort(404)
        timer.delete()
        return '', 204


@timer_ns.route('/create')
class TimerCreate(Resource):
    def get(self):
        """Display the timer creation form"""
        form = TimerForm()
        return make_response(render_template('timer_form.html', form=form), 200, {'Content-Type': 'text/html'})

    def post(self):
        """Create a new timer from the form"""
        form = TimerForm(request.form)
        if form.validate():
            new_timer = TimerData(
                name=form.name.data,
                time=form.time.data,
                isGlobal=form.global_timer.data,
                user_id=form.user_id.data if form.user_id.data else None
            ).save()

            headers = Headers()
            list_url = url_for('timerrestmix_timer_list')  # Ensure the endpoint name is correct
            headers.add('Location', list_url)
            return make_response('', 302, headers)
        else:
            return make_response(render_template('timer_form.html', form=form), 200, {'Content-Type': 'text/html'})

