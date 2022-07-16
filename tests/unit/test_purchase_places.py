from http import HTTPStatus

import server
from server import PLACES_LIMIT_PER_COMPETITION
from utils import NegativeResultError
from tests.conftest import client, mocker_clubs, mocker_competitions, valid_club


club_name = "Simply Lift"

competition = {
    "name": "Spring Festival",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "25"
}


def test_places_required_greater_than_points_club(client, mocker, valid_club, captured_templates):
    """
    GIVEN a VALID club, a Valid competition & LARGE number of places,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "welcome" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    mocker.patch('server.get_club_by_key', return_value=valid_club)
    very_large_number_of_places = 1000

    data_to_post = {
        'club': valid_club['name'],
        'competition': competition['name'],
        'places': very_large_number_of_places,
    }
    response = client.post('/purchasePlaces', data=data_to_post)

    assert response.status_code == HTTPStatus.OK
    assert b'The club does not have enough points.' in response.data

    expected_template_name = "welcome.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_places_requested_exceed_places_per_competition(client, mocker, valid_club, captured_templates):
    """
    GIVEN a VALID club, a Valid competition & number of places > limit per competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "booking" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    mocker.patch('server.get_club_by_key', return_value=valid_club)

    places_required = PLACES_LIMIT_PER_COMPETITION + 1

    data_to_post = {
        'club': club_name,
        'competition': competition['name'],
        'places': places_required,
    }
    response = client.post('/purchasePlaces', data=data_to_post)

    assert response.status_code == HTTPStatus.OK
    assert b'You cannot buy more than 12 places per competition.' in response.data

    expected_template_name = "booking.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_not_enough_places_available(client, mocker, valid_club, captured_templates):
    """
    GIVEN a VALID club, a Valid competition & places available < required places,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "booking" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    mocker.patch('server.get_club_by_key', return_value=valid_club)
    mocker.patch('server.get_competition', return_value=competition)

    competition["numberOfPlaces"] = "1"
    places_required = int(competition['numberOfPlaces']) + 1
    data_to_post = {
        'club': club_name,
        'competition': competition['name'],
        'places': places_required,
    }

    with mocker.patch('server.update_points_or_places',
                      side_effect=NegativeResultError("Negative values are not allowed")):
        response = client.post('/purchasePlaces', data=data_to_post)

        assert response.status_code == HTTPStatus.OK
        assert b'This competition does not have as many places available.' in response.data

        expected_template_name = "booking.html"
        template, context = captured_templates[0]
        assert len(captured_templates) == 1
        assert template.name == expected_template_name


# def test_not_enough_places_available(client, mocker, valid_club, captured_templates):
#     """
#     GIVEN a VALID club, a Valid competition & places available < required places,
#     WHEN the user tries to access the view route "book()",
#     THEN the user arrives on the "booking" page with an appropriate message.
#     """
#
#     mocker.patch.object(server, 'clubs', mocker_clubs)
#     mocker.patch.object(server, 'competitions', mocker_competitions)
#     mocker.patch('server.get_club_by_key', return_value=valid_club)
#     competition = {
#         "name": "Spring Festival",
#         "date": "2020-03-27 10:00:00",
#         "numberOfPlaces": "1"
#     }
#     mocker.patch('server.get_competition', return_value=competition)
#     # mocker.patch('server.update_points_or_places', return_value=(NegativeResultError))
#
#     places_required = int(competition['numberOfPlaces']) + 1
#     data = {
#         'club': club_name,
#         'competition': competition['name'],
#         'places': places_required,
#     }
#     response = client.post('/purchasePlaces', data=data)
#
#     assert response.status_code == HTTPStatus.OK
#     assert b'This competition does not have as many places available.' in response.data
#
#     expected_template_name = "booking.html"
#     template, context = captured_templates[0]
#     assert len(captured_templates) == 1
#     assert template.name == expected_template_name


def test_not_enough_places_available(client, mocker, valid_club, captured_templates):
    """
    GIVEN a VALID club, a Valid competition, places available > required places
    & total number of places requested exceeds the authorized limit,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "booking" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    mocker.patch('server.get_club_by_key', return_value=valid_club)
    mocker.patch('server.get_competition', return_value=competition)
    mocker.patch('server.update_points_or_places', return_value=15)
    mocker.patch('server.check_places_number_for_a_competition_and_update', return_value=False)

    places_required = 10
    data_to_post = {
        'club': club_name,
        'competition': competition['name'],
        'places': places_required,
    }
    response = client.post('/purchasePlaces', data=data_to_post)
    expected_phrase = f'You cannot buy more than {PLACES_LIMIT_PER_COMPETITION} places per competition.'
    assert response.status_code == HTTPStatus.OK
    assert expected_phrase in response.data.decode()

    expected_template_name = "booking.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_places_successfully_buyed(client, mocker, valid_club, captured_templates):
    """
    GIVEN a VALID club, a Valid competition, places available > required places
    & total number of places requested < the authorized limit,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "welcome" page with an appropriate message:
     -> "Great-booking complete!".
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    mocker.patch('server.get_club_by_key', return_value=valid_club)
    mocker.patch('server.get_competition', return_value=competition)
    mocker.patch('server.update_points_or_places', return_value=15)
    mocker.patch('server.check_places_number_for_a_competition_and_update', return_value=True)

    places_required = 10
    data_to_post = {
        'club': club_name,
        'competition': competition['name'],
        'places': places_required,
    }
    response = client.post('/purchasePlaces', data=data_to_post)
    assert response.status_code == HTTPStatus.OK
    assert b"Great-booking complete!" in response.data

    expected_template_name = "welcome.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name
