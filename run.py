import os

from app import app

if __name__ == '__main__':
    print(os.getenv('POMODORO_HOST', 'localhost'))
    app.run(debug=True, host=os.getenv('POMODORO_HOST', 'localhost'))
