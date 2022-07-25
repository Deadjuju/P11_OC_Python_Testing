from datetime import datetime, timedelta

import pytest

from utils import (check_places_number_for_a_competition_and_update,
                   get_club_by_key,
                   get_competition,
                   init_a_club_if_not_in_dict,
                   is_date_not_already_past,
                   update_points_or_places,
                   ClubNotFoundError,
                   CompetitionNotFoundError,
                   NegativeResultError)

tomorrow = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")


def test_should_false_for_date_in_past():
    """
    Return FALSE for a past date
    """

    date_in_past = "2020-03-27 10:00:00"
    assert not is_date_not_already_past(date_in_past)


def test_should_true_for_date_in_future():
    """
    Return TRUE for a future date
    """

    date_in_future = tomorrow
    assert is_date_not_already_past(date_in_future)


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
    with pytest.raises(ClubNotFoundError):
        get_club_by_key(clubs, invalid_mail, "email")


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
    with pytest.raises(ClubNotFoundError):
        get_club_by_key(clubs, invalid_name, "name")


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
        get_competition(competitions, invalid_name)


def test_success_to_update_points_or_places():
    assert update_points_or_places(places_required=4, current_points_or_places=7) == 3
    assert update_points_or_places(places_required=1, current_points_or_places=9) == 8


def test_fail_to_update_points_with_negative_result():
    with pytest.raises(NegativeResultError):
        update_points_or_places(places_required=4, current_points_or_places=3)


def test_should_init_a_club():
    """
    GIVEN a dictionary whose keys are club names and given a club not present in this dictionary,
    WHEN the "init_a_club_if_not_in_dict" function is apply,
    THEN the club is added to the dictionary and has the value of an empty dictionary.
    """

    club_places_per_competition = club_places_per_competition = {
        'Simply Lift': {"Super Smash Force": 1, "Fall Classic": 12}
    }
    club_name = "Lift Ting"
    expected_result = {
        'Simply Lift': {"Super Smash Force": 1, "Fall Classic": 12},
        'Lift Ting': {}
    }
    init_a_club_if_not_in_dict(club_places_per_competition, club_name)
    assert club_places_per_competition == expected_result


def test_already_in_dict_when_try_init_a_club():
    """
    GIVEN a dictionary whose keys are club names and given a club already present in this dictionary,
    WHEN the "init_a_club_if_not_in_dict" function is apply,
    THEN the dictionary remains unchanged.
    """

    club_places_per_competition = club_places_per_competition = {
        'Simply Lift': {"Super Smash Force": 1, "Fall Classic": 12}
    }
    club_name = "Simply Lift"
    expected_result = {
        'Simply Lift': {"Super Smash Force": 1, "Fall Classic": 12}
    }
    init_a_club_if_not_in_dict(club_places_per_competition, club_name)
    assert club_places_per_competition == expected_result


def test_should_true_total_places_for_a_competition_less_or_equal_than_twelve():
    """
    GIVEN sum of current_places_competition and required_places
    WHEN the sum <= 12
    THEN return True
    """

    club_places_per_competition = {
        'Simply Lift': {"Super Smash Force": 3, "Fall Classic": 12}
    }
    club_name = "Simply Lift"
    competition_name = "Super Smash Force"
    required_places = 5
    result = check_places_number_for_a_competition_and_update(club_places_per_competition,
                                                              club_name,
                                                              competition_name,
                                                              required_places)
    assert result


def test_should_false_total_places_for_a_competition_greater_than_twelve():
    """
    GIVEN sum of current_places_competition and required_places
    WHEN the sum > 12
    THEN return False
    """

    club_places_per_competition = {
        'Simply Lift': {"Super Smash Force": 6, "Fall Classic": 12}
    }
    club_name = "Simply Lift"
    competition_name = "Super Smash Force"
    required_places = 7
    # 6 + 7 = 13 > 12
    result = check_places_number_for_a_competition_and_update(club_places_per_competition,
                                                              club_name,
                                                              competition_name,
                                                              required_places)
    assert not result
