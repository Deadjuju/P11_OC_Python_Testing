from datetime import datetime, timedelta

import pytest
from utils import (get_club_by_key,
                   get_competition,
                   is_date_not_already_past,
                   update_points_or_places,
                   ClubNotFoundError,
                   CompetitionNotFoundError,
                   NegativeResultError)
from tests.conftest import clubs, competitions

tomorrow = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")


def test_should_false_for_date_in_past():
    date_in_past = "2020-03-27 10:00:00"
    assert is_date_not_already_past(date_in_past) == False


def test_should_true_for_date_in_future():
    date_in_future = tomorrow
    assert is_date_not_already_past(date_in_future) == True


def test_find_club_with_mail(clubs):
    expected_club = {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': '13'
        }
    valid_mail = "john@simplylift.co"
    club = get_club_by_key(clubs, valid_mail, "email")
    assert club == expected_club


def test_fail_to_find_club_with_bad_mail(clubs):
    invalid_mail = "coincoin@badmail.com"
    with pytest.raises(ClubNotFoundError) as e_info:
        club = get_club_by_key(clubs, invalid_mail, "email")


def test_find_club_with_name(clubs):
    expected_club = {
            'name': 'Iron Temple',
            'email': 'admin@irontemple.com',
            'points': '4'
        }
    valid_name = "Iron Temple"
    club = get_club_by_key(clubs, valid_name, "name")
    assert club == expected_club


def test_fail_to_find_club_with_bad_name(clubs):
    invalid_name = "Iron Maiden"
    with pytest.raises(ClubNotFoundError) as e_info:
        club = get_club_by_key(clubs, invalid_name, "name")


def test_get_competition(competitions):
    expected_competition = {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    }
    valid_competition_name = "Spring Festival"
    competition = get_competition(competitions, valid_competition_name)
    assert competition == expected_competition


def test_fail_to_get_competition_with_invalid_name(competitions):
    invalid_name = "Springfield"
    with pytest.raises(CompetitionNotFoundError):
        competition = get_competition(competitions, invalid_name)


def test_success_to_update_points_or_places():
    assert update_points_or_places(places_required=4, current_points_or_places=7) == 3
    assert update_points_or_places(places_required=1, current_points_or_places=9) == 8


def test_fail_to_update_points_with_negative_result():
    with pytest.raises(NegativeResultError):
        update_points_or_places(places_required=4, current_points_or_places=3)
