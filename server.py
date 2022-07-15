import json

from flask import Flask, render_template, request, redirect, flash, url_for
from markupsafe import escape

from utils import (check_places_number_for_a_competition_and_update,
                   get_club_by_key,
                   get_competition,
                   init_a_club_if_not_in_dict,
                   is_date_not_already_past,
                   update_points_or_places,
                   ClubNotFoundError,
                   CompetitionNotFoundError,
                   NegativeResultError)


PLACES_LIMIT_PER_COMPETITION: int = 12


def load_clubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']

         # Add for each competition if it has not yet passed
         for competition in list_of_competitions:
             competition["is_date_not_yet_passed"] = is_date_not_already_past(competition["date"])

         return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
club_places_per_competition = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
    Log a club
    """
    user_mail = request.form['email']
    try:
        club_to_log = get_club_by_key(clubs, user_mail, key="email")
    except ClubNotFoundError:
        error_login_message = f"Mail -- {escape(user_mail)} -- Sorry, that email wasn't found."
        flash(error_login_message)
        return redirect(url_for('index'))
    init_a_club_if_not_in_dict(club_places_per_competition, club_to_log['name'])
    return render_template('welcome.html', club=club_to_log, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        found_club = get_club_by_key(clubs, club, key="name")
    except ClubNotFoundError:
        flash("You don't exist, sorry.")
        return render_template('index.html')

    try:
        found_competition = get_competition(competitions, competition)
    except CompetitionNotFoundError:
        flash("This competition does not exist.")
        return render_template('index.html')

    if not found_competition["is_date_not_yet_passed"]:
        flash("This event has already passed.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if found_club and found_competition:
        return render_template(
            'booking.html',
            club=found_club,
            competition=found_competition,
            limit_places_per_competition=PLACES_LIMIT_PER_COMPETITION
        )
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club_name = request.form['club']
    club = get_club_by_key(clubs, club_name, key="name")
    competition = get_competition(competitions, request.form['competition'])
    competition_name = competition['name']

    current_club_points = int(club['points'])
    current_competitions_places = int(competition['numberOfPlaces'])
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

    try:
        new_competition_places = update_points_or_places(places_required, current_competitions_places)
    except NegativeResultError:
        flash('This competition does not have as many places available.')
        return render_template(
            template_name_or_list='booking.html',
            club=club,
            competition=competition,
            limit_places_per_competition=PLACES_LIMIT_PER_COMPETITION
        )

    is_places_for_competition_greater_than_twelve = check_places_number_for_a_competition_and_update(
        club_places_per_competition,
        club_name,
        competition_name,
        places_required
    )

    if is_places_for_competition_greater_than_twelve:
        competition['numberOfPlaces'] = new_competition_places
        club['points'] = update_points_or_places(places_required, current_club_points)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    flash(f'You cannot buy more than {PLACES_LIMIT_PER_COMPETITION} places per competition.')
    return render_template(
        template_name_or_list='booking.html',
        club=club,
        competition=competition,
        limit_places_per_competition=PLACES_LIMIT_PER_COMPETITION
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
