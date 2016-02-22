"""Creates the database for the life dash."""

from model import connect_to_db, db
from model import PomoMetric, Daily
from server import app

METRIC_LIST = ['energy', 'hunger', 'motivation', 'focus', 'mood']

DAILY_LIST = [['Walk Kitty', 'Take Kitty for a walk.', 3, 'dog'],
              ['15m Exercise', '15 minutes of high-intensity exercise.', 3, 'exercise'],
              ['CoQ 10', '200mg CoQ 10 per dose.', 2, 'meds'],
              ['Vitamin D3', '1000mg Vitamin D3 per dose.', 2, 'meds'],
              ['Calcium', '500mg Calcium per dose.', 2, 'meds'],
              ['Green Tea', 'Drink LOTS of green tea!', 3, 'tea'],
              ['Guinea Pig Maintenance', 'Check on & care for guinea pigs.', 1, 'guinea_pig'],
              ['Github Commit', 'Submit a useful commit to a project on Github.', 3, 'github'],
              ['5m Hamstring Stretches', '5m of moderate hamstring stretches.', 3, 'stretch'],
              ['Help Luke', 'Do something nice for Luke', 1, 'heart'],
              ['Help a Friend', 'Do something nice for a friend.', 1, 'helping_hand'],
              ['10m Brainstorm', '10 minutes of brainstorming high-value things to think about, suggest, write, etc.', 1, 'brainstorm']
              ]


def create_pomo_metrics(METRIC_LIST):
    """Creates pre-defined pomo metrics."""

    for each in METRIC_LIST:
        metric = PomoMetric(name=each)

        db.session.add(metric)

    db.session.commit()


def create_dailies(DAILY_LIST):
    """Creates pre-defined daily tasks."""

    for each in DAILY_LIST:
        daily = Daily(name=each[0],
                      desc=each[1],
                      qty=each[2],
                      icon=each[3])

        db.session.add(daily)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    create_pomo_metrics(METRIC_LIST)
    create_dailies(DAILY_LIST)
