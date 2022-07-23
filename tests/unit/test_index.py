from http import HTTPStatus


def test_should_connect_to_index(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_should_template_name_be_index(client, captured_templates):
    expected_template_name = "index.html"
    response = client.get('/')
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name
