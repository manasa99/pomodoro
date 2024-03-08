from app import app, db, TimerData

# Create 10 timers
timers = []
with app.app_context():
    for i in range(1, 11):
        name = f"Timer{i}"
        time = i * 10  # Assuming each timer has a time value based on its index
        is_global = i % 2 == 0  # Alternate timers are global
        timer = TimerData(name=name, time=time, isGlobal=is_global, user_id='admin')
        timers.append(timer)

    # Add timers to the session
    db.session.add_all(timers)
    # Commit the changes to the database
    db.session.commit()
