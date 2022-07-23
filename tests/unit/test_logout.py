from http import HTTPStatus


def test_should_redirect(client, captured_templates):
    """
    When user logout, he is automatically redirected.
    """

    response = client.get('/logout')
    assert response.status_code == HTTPStatus.FOUND


def test_should_redirect_to_index(client, captured_templates):
    """
    After logout, user redirected to index page.
    """

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    expected_template_name = "index.html"
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name
