"""Server for the life dash."""

from random import randint
from datetime import datetime, date, timedelta

from model import connect_to_db, db
from model import Pomodoro, PomoMetric, PomoScore, Daily, DailyDone, Food, Exercise, Factor

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
    today = datetime.combine(date.today(), datetime.min.time()) - timedelta(hours=24)
    tomorrow = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=28)

    # Grab current pomodoro + the metrics and dailies we'll need to build out the dash

    current_pomo = db.session.query(Pomodoro).filter(Pomodoro.finish > now).first()
    last_pomo = db.session.query(Pomodoro).filter(Pomodoro.finish < now).order_by(Pomodoro.finish.desc()).first()

    if last_pomo is not None:
        last_pomo.start_str = str(datetime.strftime(last_pomo.start, "%I:%M %p"))
        last_pomo.finish_str = str(datetime.strftime(last_pomo.finish, "%I:%M %p"))

    if current_pomo is None:
        current_pomo = db.session.query(Pomodoro).filter(Pomodoro.finish < now).filter(Pomodoro.desc == None).first()

    metrics = db.session.query(PomoMetric).all()
    dailies = db.session.query(Daily).all()

    for daily in dailies:
        daily.count = 0
        daily.colors = randint(1,3)

    # everything done in the last 12 hours should display

    pomos_done = db.session.query(Pomodoro).filter(Pomodoro.finish > today).filter(Pomodoro.finish < tomorrow).all()
    dailies_done = db.session.query(DailyDone).filter(DailyDone.time > today).filter(DailyDone.time < tomorrow).all()

    for done in dailies_done:
        for daily in dailies:
            if daily.id == done.daily_id:
                daily.count += 1
                break

    food = db.session.query(Food).filter(Food.time > today).filter(Food.time < tomorrow).all()
    exercise = db.session.query(Exercise).filter(Exercise.time > today).filter(Exercise.time < tomorrow).all()
    factors = db.session.query(Factor).filter(Factor.time > today).filter(Factor.time < tomorrow).all()

    return render_template('index.html', current_pomo=current_pomo,
                                         last_pomo=last_pomo,
                                         metrics=metrics,
                                         dailies=dailies,
                                         pomos_done=pomos_done,
                                         dailies_done=dailies_done,
                                         food=food,
                                         exercise=exercise,
                                         factors=factors)


@app.route('/complete', methods=['POST'])
def complete_daily():
    """Daily task completion handling."""

    daily_id = request.form.get("daily_id")

    daily = DailyDone(daily_id=daily_id)

    db.session.add(daily)
    db.session.commit()

    return "done"


@app.route('/start-pomo', methods=['POST'])
def start_pomo():
    """Start a new pomodoro."""

    raw_start = request.form.get("pomo_start").split()
    raw_end = request.form.get("pomo_end").split()

    raw_start = ' '.join(raw_start[0:5])
    raw_end = ' '.join(raw_end[0:5])

    pomo_start = datetime.strptime(raw_start, "%a %b %d %Y %X")
    pomo_end = datetime.strptime(raw_end, "%a %b %d %Y %X")

    pomo = Pomodoro(start=pomo_start, finish=pomo_end)

    db.session.add(pomo)
    db.session.flush()
    db.session.commit()

    return pomo.id

@app.route('/submit-pomo', methods=['POST'])
def submit_pomo():
    """Submit pomodoro to db."""

    pomo_id = request.form.get("pomo_id")
    pomo_desc = request.form.get("pomo_desc")

    pomo_end = request.form.get("pomo_end").split()
    pomo_end = ' '.join(pomo_end[0:5])
    pomo_end = datetime.strptime(pomo_end, "%a %b %d %Y %X")

    current_pomo = db.session.query(Pomodoro).filter(Pomodoro.id == pomo_id).one()
    current_pomo.desc = pomo_desc
    current_pomo.finish = pomo_end

    score_mood = request.form.get("mood")
    mood_id = db.session.query(PomoMetric).filter(PomoMetric.name == 'mood').one()
    mood = PomoScore(metric_id=mood_id.id, pomo_id=pomo_id, score=score_mood)
    db.session.add(mood)

    score_motivation = request.form.get("motivation")
    motivation_id = db.session.query(PomoMetric).filter(PomoMetric.name == 'motivation').one()
    motivation = PomoScore(metric_id=motivation_id.id, pomo_id=pomo_id, score=score_motivation)
    db.session.add(motivation)

    score_focus = request.form.get("focus")
    focus_id = db.session.query(PomoMetric).filter(PomoMetric.name == 'focus').one()
    focus = PomoScore(metric_id=focus_id.id, pomo_id=pomo_id, score=score_focus)
    db.session.add(focus)

    score_energy = request.form.get("energy")
    energy_id = db.session.query(PomoMetric).filter(PomoMetric.name == 'energy').one()
    energy = PomoScore(metric_id=energy_id.id, pomo_id=pomo_id, score=score_energy)
    db.session.add(energy)

    score_hunger = request.form.get("hunger")
    hunger_id = db.session.query(PomoMetric).filter(PomoMetric.name == 'hunger').one()
    hunger = PomoScore(metric_id=hunger_id.id, pomo_id=pomo_id, score=score_hunger)
    db.session.add(hunger)

    db.session.commit()

    return jsonify({'success': 'yes'})


@app.route('/submit-food', methods=['POST'])
def submit_food():
    """Submit food entry to db."""

    desc = request.form.get("desc")
    calories = int(request.form.get("calories"))

    food = Food(desc=desc, calories=calories)
    db.session.add(food)
    db.session.commit()

    return jsonify({'success': 'yes'})


@app.route('/submit-exercise', methods=['POST'])
def submit_exercise():
    """Submit exercise entry to db."""

    desc = request.form.get("desc")
    duration = int(request.form.get("duration"))
    intensity = request.form.get("intensity")
    calories = int(request.form.get("calories"))

    exercise = Exercise(desc=desc, duration=duration, intensity=intensity, calories=calories)
    db.session.add(exercise)
    db.session.commit()

    return jsonify({'success': 'yes'})


@app.route('/submit-misc', methods=['POST'])
def submit_misc():
    """Submit misc factor entry to db."""

    desc = request.form.get("desc")
    name = request.form.get("name")

    factor = Factor(desc=desc, name=name)
    db.session.add(factor)
    db.session.commit()

    return jsonify({'success': 'yes'})


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
