"""Classes for the life dash."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    def __init__(self):
        self.start = datetime.now()


class Daily(db.Model):
    """Daily activity option."""

    __tablename__ = "dailies"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Daily id={} name={} desc={} qty={}>".format(self.id,
                                                             self.name,
                                                             self.desc,
                                                             self.qty)

    def __init__(self, name, desc='No description.', qty=1):
        self.name = name
        self.desc = desc
        self.qty = qty


class DailyDone(db.Model):
    """Daily completion info."""

    __tablename__ = "dailies_done"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    daily_id = db.Column(db.Integer, db.ForeignKey('dailies.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<DailyDone id={} daily_id={} complete_time={}".format(self.id,
                                                                      self.daily_id,
                                                                      self.time)

    def __init__(self, daily_id):
        self.daily_id = daily_id
        self.complete_time = datetime.now()


class Food(db.Model):
    """Food log entry."""

    __tablename__ = "food"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(500), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Food id={} calories={} desc={} time={}>".format(self.id,
                                                                 self.desc,
                                                                 self.calories,
                                                                 self.time)

    def __init__(self, desc, calories):
        self.desc = desc
        self.calories = calories
        self.time = datetime.now()


class Exercise(db.Model):
    """Exercise log entry."""

    __tablename__ = "exercises"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(500), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Exercise id={} calories={} intensity={} duration={} desc={} time={}>".format(self.id,
                                                                                              self.calories,
                                                                                              self.intensity,
                                                                                              self.duration,
                                                                                              self.desc,
                                                                                              self.time)

    def __init__(self, desc, calories, intensity, duration):
        self.desc = desc
        self.calories = calories
        self.intensity = intensity
        self.duration = duration


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