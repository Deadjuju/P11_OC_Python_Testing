from datetime import datetime, timedelta

from utils import is_date_not_already_past

tomorrow = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")


def test_should_false_for_date_in_past():
    date_in_past = "2020-03-27 10:00:00"
    assert is_date_not_already_past(date_in_past) == False


def test_should_true_for_date_in_future():
    date_in_future = tomorrow
    assert is_date_not_already_past(date_in_future) == True
