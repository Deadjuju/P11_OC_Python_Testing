from datetime import datetime, timedelta

import pytest
from utils import get_club_by_key, is_date_not_already_past, ClubNotFoundError
from tests.conftest import clubs

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
