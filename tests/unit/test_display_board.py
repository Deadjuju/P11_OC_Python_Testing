from http import HTTPStatus

import server
from tests.conftest import Templates, Urls, mocker_clubs, mocker_competitions


def test_route_display_board(mocker, client, captured_templates):
    """
    Display of clubs using template "display-board.html"
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get(Urls.DISPLAY_BOARD.value)
    template, context = captured_templates[0]

    assert response.status_code == HTTPStatus.OK
    for club in mocker_clubs:
        message = f"Club: {club['name']} - {club['points']} points"
        assert message in response.data.decode()
    assert len(captured_templates) == 1
    assert template.name == Templates.DISPLAY_BOARD.value
