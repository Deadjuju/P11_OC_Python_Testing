from http import HTTPStatus

import server
from tests.conftest import Templates, Urls, mocker_clubs, mocker_competitions


def test_book_for_passed_competition(client, mocker, valid_club, past_competition, captured_templates):
    """
    GIVEN a VALID club & PAST competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "welcome" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(Urls.booking_url(competition=past_competition['name'],
                                           club=valid_club['name']))
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert b"This event has already passed." in response.data
    assert len(captured_templates) == 1
    assert template.name == Templates.WELCOME.value


def test_book_with_invalid_club(client, mocker, invalid_club, future_competition, captured_templates):
    """
    GIVEN an INVALID club & FUTURE competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "index" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(Urls.booking_url(competition=future_competition['name'],
                                           club=invalid_club['name']))
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert b"You don&#39;t exist, sorry." in response.data
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value


def test_book_with_invalid_competition(client, mocker, valid_club, future_competition, captured_templates):
    """
    GIVEN a VALID club & invalid competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "index" page with an appropriate message.
    """

    invalid_competition_name = f"XXXX{future_competition['name']}XXXX"

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(Urls.booking_url(competition=invalid_competition_name,
                                           club=valid_club['name']))
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert b"This competition does not exist." in response.data
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value


def test_book_with_valid_club_and_valid_future_competition(client,
                                                           mocker,
                                                           valid_club,
                                                           future_competition,
                                                           captured_templates):
    """
    GIVEN a VALID club & FUTURE competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "booking" page.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(Urls.booking_url(competition=future_competition['name'],
                                           club=valid_club['name']))
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert len(captured_templates) == 1
    assert template.name == Templates.BOOKING.value
