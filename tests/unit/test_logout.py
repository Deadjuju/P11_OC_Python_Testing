from http import HTTPStatus

from tests.conftest import Templates, Urls


def test_should_redirect(client, captured_templates):
    """
    When user logout, he is automatically redirected.
    """

    response = client.get(Urls.LOGOUT.value)
    assert response.status_code == HTTPStatus.FOUND


def test_should_redirect_to_index(client, captured_templates):
    """
    After logout, user redirected to index page.
    """

    response = client.get(Urls.LOGOUT.value, follow_redirects=True)
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value
