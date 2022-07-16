from http import HTTPStatus

from server import show_summary
import server
from tests.conftest import client, mocker_clubs


def test_log_with_valid_mail(client, mocker, captured_templates):
    """
    GIVEN a valid mail,
    WHEN club try to log it,
    THEN the club arrives on the "welcome" page.
    """

    valid_mail = "john@simplylift.co"
    expected_welcome_phrase = f"Welcome, {valid_mail}"
    mocker.patch.object(server, 'clubs', mocker_clubs)

    response = client.post('/showSummary', data={"email": valid_mail})
    assert response.status_code == HTTPStatus.OK
    assert expected_welcome_phrase in response.data.decode()

    expected_template_name = "welcome.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_log_with_invalid_email(client, mocker, captured_templates):
    """
    GIVEN a invalid mail,
    WHEN club try to log it,
    THEN the club arrives on the "index" page.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    unknown_user = {"email": "obiwan@jedi.tato"}
    response = client.post('/showSummary', data=unknown_user)

    assert response.status_code == HTTPStatus.OK

    expected_template_name = "index.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name


def test_not_allowed_with_get(client, mocker):
    """
    GET method is not allowed
    """

    response = client.get("/showSummary")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
