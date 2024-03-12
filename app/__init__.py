import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_DB', 'sqlite:///pomodoro.db')
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views.timer_routes import *
from app.views.timer_views import *
from app.views.timer_bp import *
# from app.views.all_routes import *

app.register_blueprint(timer_bp)
# app.register_blueprint(timer_blueprint)

app.add_url_rule('/', view_func=hello, methods=['GET'])
app.add_url_rule('/<name>', view_func=hello, methods=['GET'])


timer_view = TimerDataAPI.as_view('timer_api')
app.add_url_rule('/timerview', view_func=timer_view, methods=['GET', 'POST'])
app.add_url_rule('/timerview/<int:timer_id>', view_func=timer_view, methods=['GET', 'PUT', 'DELETE'])
