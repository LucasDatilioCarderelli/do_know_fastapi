from http import HTTPStatus

from jwt import decode

from do_know_fastapi.security import create_access_token
from do_know_fastapi.settings import Settings

settings = Settings()


def test_jwt():
    data = {'sub': 'test@test.com'}
    result = create_access_token(data)

    result = decode(
        result, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert 'exp' in result


def test_jwt_invalid(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
