"""Creates the database for the life dash."""

from model import connect_to_db, db
from server import app

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
