from http import HTTPStatus

from tests.conftest import Templates, Urls, mocker_clubs
import server


def test_go_to_display_board(client, mocker, captured_templates, valid_club, future_competition):
    """
    • the user connects to the site,
    • and goes to display board page
    """

    mocker.patch.object(server, 'clubs', mocker_clubs)
    template_number: int = 0

    # 1. user arrivers on index page
    template_number += 1
    index_response = client.get(Urls.INDEX.value)
    template, context = captured_templates[template_number - 1]

    assert index_response.status_code == HTTPStatus.OK
    assert len(captured_templates) == template_number
    assert template.name == Templates.INDEX.value

    # 2. user goes to display board page
    template_number += 1
    board_response = client.get(Urls.DISPLAY_BOARD.value)
    template, context = captured_templates[template_number - 1]

    assert board_response.status_code == HTTPStatus.OK
    for club in mocker_clubs:
        message = f"Club: {club['name']} - {club['points']} points"
        assert message in board_response.data.decode()
    assert len(captured_templates) == template_number
    assert template.name == Templates.DISPLAY_BOARD.value
