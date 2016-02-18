"""Classes for the life dash."""

from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy()


class Pomodoro(db.Model):
    """Pomodoro details"""

    __tablename__ = "pomodoros"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    start = db.Column(db.DateTime, nullable=False)
    finish = db.Column(db.DateTime, nullable=True)
    desc = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Pomodoro id={} start={} finish={} desc={}>".format(self.id,
                                                                    self.start,
                                                                    self.finish,
                                                                    self.desc)

    def __init__(self, start):
        self.start = start


class Daily(db.Model):
    """Daily activity option."""

    __tablename__ = "dailies"

    id = db.Column(db.Integer, nullable-False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Daily id={} name={} desc={} qty={}>".format(self.id,
                                                             self.name,
                                                             self.desc,
                                                             self.qty)

class DailyDone(db.Model):
    """Daily completion info."""

    __tablename__ = "dailies_done"

    # TODO


# TODO: food + exercise classes



##############################################################################
# Helper functions


def connect_to_db(app, db_uri="sqlite:///masondash.db"):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


##############################################################################