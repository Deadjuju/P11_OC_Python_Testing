import pprint
from http import HTTPStatus

from flask.helpers import url_for

from tests.conftest import client, mocker_clubs
import server

TEMPLATE_INDEX = "index.html"
TEMPLATE_WELCOME = "welcome.html"
VALID_MAIL = "john@simplylift.co"


def test_login(client, mocker, captured_templates):
    """
    From index page the club can log in with a valid mail and arrives to welcome page
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)

    # index page
    response = client.get('/')
    log_in_url = url_for("show_summary")
    assert response.status_code == HTTPStatus.OK

    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == TEMPLATE_INDEX

    # log in
    log_link = f'action="{log_in_url}"'
    assert log_link in response.data.decode()

    response = client.post(log_in_url, data={"email": VALID_MAIL})
    assert response.status_code == HTTPStatus.OK
    assert VALID_MAIL in response.data.decode()

    template, context = captured_templates[1]
    assert len(captured_templates) == 2
    assert template.name == TEMPLATE_WELCOME


def test_log_out_when_club_is_log(mocker, client, captured_templates):
    """
    The club is already log.
    Test logout: redirection and the club arrives on index page
    """
    mocker.patch.object(server, 'clubs', mocker_clubs)

    # log with a valid mail
    response = client.post("/showSummary", data={"email": VALID_MAIL})
    assert response.status_code == HTTPStatus.OK
    assert VALID_MAIL in response.data.decode()

    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == TEMPLATE_WELCOME

    # redirect
    url_log_out = url_for("logout")
    logout_link = f'href="{url_log_out}"'
    assert logout_link in response.data.decode()
    response = client.get(url_log_out)
    assert response.status_code == HTTPStatus.FOUND

    # log out
    response = client.get(url_log_out, follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    template, context = captured_templates[1]
    assert len(captured_templates) == 2
    assert template.name == TEMPLATE_INDEX
