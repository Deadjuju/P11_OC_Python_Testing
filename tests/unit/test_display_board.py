from http import HTTPStatus

import server
from tests.conftest import captured_templates, client, mocker_clubs, mocker_competitions


def test_route_display_board(mocker, client, captured_templates):
    """
    Display of clubs using template "display-board.html"
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_competitions)

    response = client.get("/points-display-board")

    assert response.status_code == HTTPStatus.OK
    for club in mocker_clubs:
        message = f"Club: {club['name']} - {club['points']} points"
        assert message in response.data.decode()

    expected_template_name = "display-board.html"
    template, context = captured_templates[0]

    assert len(captured_templates) == 1
    assert template.name == expected_template_name
