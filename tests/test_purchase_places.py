import server
from tests.conftest import client, mocker_clubs, mocker_competitions


club_name = "Simply Lift"

competition = {
    "name": "Spring Festival",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "25"
}


def test_places_required_greater_than_points_club(client, mocker):

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    data = {
        'club': club_name,
        'competition': competition['name'],
        'places': 1000,
    }
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'The club does not have enough points.' in response.data


def test_limits_of_places_per_club_exceeded(client, mocker):
    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    data = {
        'club': club_name,
        'competition': competition['name'],
        'places': 13,
    }
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'You cannot buy more than 12 places per competition.' in response.data


def test_places_successfully_buyed(client, mocker):

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    data = {
        'club': club_name,
        'competition': competition['name'],
        'places': 2,
    }
    response = client.post('/purchasePlaces', data=data)

    places_required = int(data['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required

    assert competition['numberOfPlaces'] == 23
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
