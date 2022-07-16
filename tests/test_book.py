from http import HTTPStatus

import server
from tests.conftest import (captured_templates,
                            client,
                            future_competition,
                            invalid_club,
                            mocker_clubs,
                            mocker_competitions,
                            past_competition,
                            valid_club)


def test_book_for_passed_competition(client, mocker, valid_club, past_competition, captured_templates):
    """
    GIVEN a VALID club & PAST competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "welcome" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{past_competition['name']}/{valid_club['name']}")

    assert response.status_code == HTTPStatus.OK
    assert b"This event has already passed." in response.data

    expected_template_name = "welcome.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_book_with_invalid_club(client, mocker, invalid_club, future_competition, captured_templates):
    """
    GIVEN an INVALID club & FUTURE competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "index" page with an appropriate message.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{future_competition['name']}/{invalid_club['name']}")

    assert response.status_code == HTTPStatus.OK
    assert b"You don&#39;t exist, sorry." in response.data

    expected_template_name = "index.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name



def test_book_with_invalid_competition(client, mocker, valid_club, future_competition, captured_templates):
    """
    GIVEN a VALID club & FUTRURE competition,
    WHEN the user tries to access the view route "book()",
    THEN the user arrives on the "index" page with an appropriate message.
    """

    invalid_competition_name = f"XXXX{future_competition['name']}XXXX"

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{invalid_competition_name}/{valid_club['name']}")

    assert response.status_code == HTTPStatus.OK
    assert b"This competition does not exist." in response.data

    expected_template_name = "index.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


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

    response = client.get(f"/book/{future_competition['name']}/{valid_club['name']}")

    assert response.status_code == HTTPStatus.OK

    expected_template_name = "booking.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name
