from enum import Enum

from flask import template_rendered
import pytest

from server import app


class Templates(Enum):
    """
    name of templates used
    """

    INDEX = "index.html"
    WELCOME = "welcome.html"
    BOOKING = "booking.html"
    DISPLAY_BOARD = "display-board.html"


class Urls(Enum):
    """
    urls used in the application
    """

    INDEX = "/"
    LOGIN = "/showSummary"
    BOOKING = "/book"
    PURCHASE_PLACES = "/purchasePlaces"
    LOGOUT = "/logout"
    DISPLAY_BOARD = "/points-display-board"

    @classmethod
    def booking_url(cls, competition: str, club: str) -> str:
        return f"{cls.BOOKING.value}/{competition}/{club}"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def captured_templates():
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


mocker_clubs = [
    {
        'name': 'Simply Lift',
        'email': 'john@simplylift.co',
        'points': '13'
    },
    {
        'name': 'Iron Temple',
        'email': 'admin@irontemple.com',
        'points': '4'
    },
    {
        'name': 'She Lifts',
        'email': 'kate@shelifts.co.uk',
        'points': '12'
    },
    {
        'name': 'Club With Many Points',
        'email': 'i_have_a_lot@of.points',
        'points': '9999'
    }
]

mocker_competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            "is_date_not_yet_passed": False
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
            "is_date_not_yet_passed": False
        },
        {
            "name": "Super Smash Force",
            "date": "3000-10-22 13:30:00",
            "numberOfPlaces": "18",
            "is_date_not_yet_passed": True
        }
    ]


@pytest.fixture
def clubs():
    return [
        {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': '13'
        },
        {
            'name': 'Iron Temple',
            'email': 'admin@irontemple.com',
            'points': '4'
        },
        {
            'name': 'She Lifts',
            'email': 'kate@shelifts.co.uk',
            'points': '12'
        },
        {
            'name': 'Club With Many Points',
            'email': 'i_have_a_lot@of.points',
            'points': '9999'
        }
    ]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Super Smash Force",
            "date": "3000-10-22 13:30:00",
            "numberOfPlaces": "18"
        }
    ]


@pytest.fixture
def valid_club(clubs):
    return clubs[0]


@pytest.fixture
def club_with_many_points(clubs):
    return clubs[3]


@pytest.fixture
def invalid_club():
    return {
        'name': 'Bad Name',
        'email': 'totally@invented.mail',
        'points': '13'
    }


@pytest.fixture
def past_competition(competitions):
    return competitions[0]


@pytest.fixture
def future_competition(competitions):
    return competitions[2]
