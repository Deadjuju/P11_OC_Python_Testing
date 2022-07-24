from http import HTTPStatus

from tests.conftest import Templates, Urls


def test_should_connect_to_index(client, captured_templates):
    """
    When the user connects to the url of the index
    The user arrives at the right place with the right template
    """

    response = client.get(Urls.INDEX.value)
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data
    assert len(captured_templates) == 1
    assert template.name == Templates.INDEX.value
