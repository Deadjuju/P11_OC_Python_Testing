import server
from tests.conftest import client, mocker_clubs, mocker_competitions


club = mocker_clubs[0]
passed_competition = mocker_competitions[0]
futur_competition = mocker_competitions[2]


def test_book_for_passed_competition(client, mocker):

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{passed_competition['name']}/{club['name']}")

    assert response.status_code == 200
    assert b"This event has already passed." in response.data

def test_book_with_invalid_club(client, mocker):

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{futur_competition['name']}/{club['name']}XXX")

    assert response.status_code == 200
    assert b"You don&#39;t exist, sorry." in response.data


def test_book_with_invalid_competition(client, mocker):

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(f"/book/{futur_competition['name']}XXXX/{club['name']}")

    assert response.status_code == 200
    assert b"This competition does not exist." in response.data
