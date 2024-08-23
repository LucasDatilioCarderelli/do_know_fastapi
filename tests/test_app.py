from http import HTTPStatus

from fastapi.testclient import TestClient

from do_know_fastapi.app import app


def test_app():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olar World'}
