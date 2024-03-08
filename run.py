import os

from app import app

if __name__ == '__main__' or __name__ == 'app':
    app.run(debug=app.config['DEBUG'], host=os.getenv('POMODORO_HOST', 'localhost'), port='5002')
