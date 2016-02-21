"""Server for the life dash."""

import random
from datetime import datetime, timedelta

from model import connect_to_db, db
from model import Pomodoro, PomoMetric, Daily, DailyDone, Food, Exercise, Factor

from jinja2 import StrictUndefined
from flask import Flask, Markup, render_template, redirect, request, flash, session, jsonify, url_for, abort
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Functions not associated with particular routes
#################################################################################


#################################################################################

@app.route('/')
def index():
    """Home / main dash."""

    now = datetime.now()

    # Grab current pomodoro + the metrics and dailies we'll need to build out the dash

    current_pomo = db.session.query(Pomodoro).filter(Pomodoro.finish is None).first()
    metrics = db.session.query(PomoMetric).all()
    dailies = db.session.query(Daily).all()

    # everything done in the last 12 hours should display

    pomos_done = db.session.query(Pomodoro).filter((now - Pomodoro.finish) < timedelta(hours=12)).all()
    dailies_done = db.session.query(DailyDone).filter((now - DailyDone.time) < timedelta(hours=12)).all()

    food = db.session.query(Food).filter((now - Food.time) < timedelta(hours=12)).all()
    exercise = db.session.query(Exercise).filter((now - Exercise.time) < timedelta(hours=12)).all()
    factors = db.session.query(Factor).filter((now - Factor.time) < timedelta(hours=12)).all()

    return render_template('index.html', current_pomo=current_pomo,
                                         metrics=metrics,
                                         dailies=dailies,
                                         pomos_done=pomos_done,
                                         dailies_done=dailies_done,
                                         food=food,
                                         exercise=exercise,
                                         factors=factors)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
