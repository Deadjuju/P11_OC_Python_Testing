from server import show_summary
import server
from tests.conftest import client, mocker_clubs


def test_log_with_valid_email(client, mocker):
    expected_status_ok = 200

    mocker.patch.object(server, 'clubs', mocker_clubs)
    user = {"email": "john@simplylift.co"}
    response = client.post('/showSummary', data=user)
    assert response.status_code == expected_status_ok


def test_log_with_invalid_email(client, mocker):
    expected_redirection_response = 302

    mocker.patch.object(server, 'clubs', mocker_clubs)
    unknown_user = {"email": "obiwan@jedi.tato"}
    response = client.post('/showSummary', data=unknown_user)
    assert response.status_code == expected_redirection_response
