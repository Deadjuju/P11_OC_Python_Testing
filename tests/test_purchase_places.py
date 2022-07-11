from tests.conftest import client

mocker_club = {
    'name': 'Simply Lift',
    'email': 'john@simplylift.co',
    'points': '13'
}

mocker_competition = {
    "name": "Spring Festival",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "25"
}


def test_places_required_greater_than_points_club(client):

    data = {
        'club': mocker_club['name'],
        'competition': mocker_competition['name'],
        'places': 1000,
    }
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'The club does not have enough points.' in response.data


def test_places_successfully_buyed(client):

    data = {
        'club': mocker_club['name'],
        'competition': mocker_competition['name'],
        'places': 2,
    }
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
