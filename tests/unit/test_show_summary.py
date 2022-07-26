from http import HTTPStatus

import server
from tests.conftest import Templates, Urls, mocker_clubs


def test_log_with_valid_mail(client, mocker, captured_templates, valid_club):
    """
    GIVEN a valid mail,
    WHEN club try to log it,
    THEN the club arrives on the "welcome" page.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    valid_mail = valid_club["email"]

    response = client.post(Urls.LOGIN.value, data={"email": valid_mail})
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert f"Welcome, {valid_mail}" in response.data.decode()
    assert len(captured_templates) == 1
    assert template.name == Templates.WELCOME.value


def test_log_with_invalid_email(client, mocker, captured_templates, invalid_club):
    """
    GIVEN a invalid mail,
    WHEN club try to log it,
    THEN the club arrives on the "index" page.
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)

    response = client.post(Urls.LOGIN.value, data={"email": invalid_club["email"]})
    template, context = captured_templates[0]
    print("/" * 500)
    print(response.data.decode())

    assert response.status_code == HTTPStatus.OK
    assert "Sorry, that email wasn&#39;t found." in response.data.decode()
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value


def test_not_allowed_with_get(client):
    """
    GET method is not allowed
    """

    response = client.get(Urls.LOGIN.value)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
