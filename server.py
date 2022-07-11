import json

from flask import Flask, render_template, request, redirect, flash, url_for
from markupsafe import escape


PLACES_LIMIT_PER_COMPETITION: int = 12


def load_clubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def show_summary():
    """
    Log a club
    """
    club_to_log = None
    user_mail = request.form['email']
    for club in clubs:
        if club['email'] == user_mail:
            club_to_log = club
    if club_to_log is None:
        error_login_message = f"Mail -- {escape(user_mail)} -- Sorry, that email wasn't found."
        flash(error_login_message)
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club_to_log, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition,
            limit_places_per_competition=PLACES_LIMIT_PER_COMPETITION
        )
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    current_club_points = int(club['points'])
    places_required = int(request.form['places'])

    if places_required > current_club_points:
        flash('The club does not have enough points.')
        return render_template('welcome.html', club=club, competitions=competitions)

    if places_required > PLACES_LIMIT_PER_COMPETITION:
        flash(f'You cannot buy more than {PLACES_LIMIT_PER_COMPETITION} places per competition.')
        return render_template(
            template_name_or_list='booking.html',
            club=club,
            competition=competition,
            limit_places_per_competition=PLACES_LIMIT_PER_COMPETITION
        )

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
