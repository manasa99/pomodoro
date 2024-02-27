import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_DB', 'sqlite:///pomodoro.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes.timer_routes import *



