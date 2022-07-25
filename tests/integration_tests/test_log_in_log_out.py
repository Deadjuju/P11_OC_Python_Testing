from http import HTTPStatus

from tests.conftest import Templates, Urls, mocker_clubs
import server


def test_login(client, mocker, captured_templates, valid_club):
    """
    From index page the club can log in with a valid mail and arrives to welcome page
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    valid_mail = valid_club['email']

    # index page
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK

    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value

    # log in
    log_link = f'action="{Urls.LOGIN.value}"'
    assert log_link in response.data.decode()

    response = client.post(Urls.LOGIN.value, data={"email": valid_mail})
    assert response.status_code == HTTPStatus.OK
    assert valid_mail in response.data.decode()

    template, context = captured_templates[1]
    assert len(captured_templates) == 2
    assert template.name == Templates.WELCOME.value


def test_log_out_when_club_is_log(mocker, client, captured_templates, valid_club):
    """
    The club is already log.
    Test logout: redirection and the club arrives on index page
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    valid_mail = valid_club['email']

    # log with a valid mail
    response = client.post(Urls.LOGIN.value, data={"email": valid_mail})
    assert response.status_code == HTTPStatus.OK
    assert valid_mail in response.data.decode()

    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == Templates.WELCOME.value

    # redirect
    logout_link = f'href="{Urls.LOGOUT.value}"'
    assert logout_link in response.data.decode()
    response = client.get(Urls.LOGOUT.value)
    assert response.status_code == HTTPStatus.FOUND

    # log out
    response = client.get(Urls.LOGOUT.value, follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    template, context = captured_templates[1]
    assert len(captured_templates) == 2
    assert template.name == Templates.INDEX.value
