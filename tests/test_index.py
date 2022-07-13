from tests.conftest import client, captured_templates


def test_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_template_index(client, captured_templates):
    expected_template_name = "index.html"
    response = client.get('/')
    template, context = captured_templates[0]
    assert len(captured_templates) == 1
    assert template.name == expected_template_name
