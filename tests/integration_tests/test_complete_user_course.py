from http import HTTPStatus

from tests.conftest import Templates, Urls, mocker_clubs, mocker_competitions
from server import NUMBERS_OF_POINTS_PER_PLACE
import server


def test_complete_course(client, mocker, captured_templates, valid_club, future_competition):
    """
    • the user connects to the site,
    • identifies himself with a valid email,
    • selects a competition in the future,
    • reserves a valid number of place
    • and logs out.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)
    template_number: int = 0

    # 1. user arrivers on index page
    template_number += 1
    index_response = client.get(Urls.INDEX.value)
    template, context = captured_templates[template_number - 1]

    assert index_response.status_code == HTTPStatus.OK
    assert len(captured_templates) == template_number
    assert template.name == Templates.INDEX.value
    assert b"Welcome to the GUDLFT Registration Portal!" in index_response.data

    # 2. Connection with valid mail
    template_number += 1
    connection_response = client.post(Urls.LOGIN.value, data={"email": valid_club['email']})
    template, context = captured_templates[template_number - 1]

    assert connection_response.status_code == HTTPStatus.OK
    assert valid_club['email'] in connection_response.data.decode()
    assert len(captured_templates) == template_number
    assert template.name == Templates.WELCOME.value

    # 3. Booking page
    template_number += 1
    booking_response = client.get(Urls.booking_url(competition=future_competition['name'],
                                                   club=valid_club['name']))
    template, context = captured_templates[template_number - 1]

    assert booking_response.status_code == HTTPStatus.OK
    assert valid_club['name'] in booking_response.data.decode()
    assert len(captured_templates) == template_number
    assert template.name == Templates.BOOKING.value

    # 4. Purchase places
    template_number += 1
    places_required = int(valid_club['points']) // NUMBERS_OF_POINTS_PER_PLACE
    data_to_post = {
        'club': valid_club['name'],
        'competition': future_competition['name'],
        'places': places_required,
    }
    places_response = client.post(Urls.PURCHASE_PLACES.value, data=data_to_post)
    template, context = captured_templates[template_number - 1]

    assert places_response.status_code == HTTPStatus.OK
    assert b"Great-booking complete!" in places_response.data
    assert len(captured_templates) == template_number
    assert template.name == Templates.WELCOME.value

    # 5. Logout
    template_number += 1
    logout_response = client.get(Urls.LOGOUT.value, follow_redirects=True)
    template, context = captured_templates[template_number - 1]

    assert logout_response.status_code == HTTPStatus.OK
    assert b"Welcome to the GUDLFT Registration Portal!" in logout_response.data
    assert len(captured_templates) == template_number
    assert template.name == Templates.INDEX.value
