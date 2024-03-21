import pytest
from flask_testing import TestCase

import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from app import app,db
from app.models.models import TimerData
class TestTimerAPI(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_timers_empty(self):
        response = self.client.get('/api/timerrest/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_timer(self):
        timer_data = {'name': 'Test Timer', 'time': 60, 'isGlobal': True, 'user_id': None}
        response = self.client.post('/api/timerrest/', json=timer_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TimerData.query.count(), 1)

    def test_get_timer(self):
        # First, create a timer to fetch
        new_timer = TimerData(name='Test Timer', time=60, isGlobal=True, user_id=None)
        db.session.add(new_timer)
        db.session.commit()
        req = f'/api/timerrest/{new_timer.id}'
        response = self.client.get(req)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Timer')

    def test_update_timer(self):
        # Create a timer to update
        new_timer = TimerData(name='Old Name', time=30, isGlobal=False, user_id='user1')
        db.session.add(new_timer)
        db.session.commit()

        update_data = {'name': 'New Name', 'time': 45, 'isGlobal': True, 'user_id': 'user2'}
        response = self.client.put(f'/api/timerrest/{new_timer.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_timer = TimerData.query.first()
        self.assertEqual(updated_timer.name, 'New Name')

    def test_delete_timer(self):
        # Create a timer to delete
        new_timer = TimerData(name='Delete Me', time=15, isGlobal=True, user_id=None)
        db.session.add(new_timer)
        db.session.commit()
        response = self.client.delete(f'/api/timerrest/{new_timer.id}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(TimerData.query.count(), 0)

    # Add more tests as needed

# Run the tests
if __name__ == '__main__':
    pytest.main()
