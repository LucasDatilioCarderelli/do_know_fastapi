from http import HTTPStatus


def test_login_for_access_token(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'Bearer'


def test_login_for_access_token_invalid(client):
    response = client.post(
        '/auth/token/',
        data={
            'username': 'wrong@test.com',
            'password': 'wrong',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
