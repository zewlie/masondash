"""Creates the database for the life dash."""

from model import connect_to_db, db
from model import Daily
from server import app


DAILY_LIST = [['Walk Kitty', 'Take Kitty for a walk.', 3],
              ['15m Exercise', '15 minutes of high-intensity exercise.', 3],
              ['CoQ 10', '200mg CoQ 10 per dose.', 2],
              ['Vitamin D3', '1000mg Vitamin D3 per dose.', 2],
              ['Calcium', '500mg Calcium per dose.', 2],
              ['Green Tea', 'Drink LOTS of green tea!', 3]
              ]


def create_dailies(DAILY_LIST):
    """Creates pre-defined daily tasks."""

    for daily in DAILY_LIST:
        daily = Daily(name=daily[0],
                      desc=daily[1],
                      qty=daily[2])

        db.session.add(daily)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    create_dailies()
