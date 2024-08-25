from http import HTTPStatus

from do_know_fastapi.schemas import UserPublicSchema


def test_app(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olar World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': 'email@email.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_conflict_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': 'user@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_conflict_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user2',
            'email': 'user@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_users_with_users(client, users):
    users_schema = [
        UserPublicSchema.model_validate(user).model_dump() for user in users
    ]

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': users_schema}


def test_read_users_with_limit(client, users):
    users_schema = [
        UserPublicSchema.model_validate(user).model_dump() for user in users
    ]

    response = client.get('/users/?limit=2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': users_schema[:2]}


def test_read_users_with_offset(client, users):
    users_schema = [
        UserPublicSchema.model_validate(user).model_dump() for user in users
    ]

    response = client.get('/users/?offset=1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': users_schema[1:]}


def test_read_users_by_id(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_users_by_id_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_client(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'newuser',
            'email': 'newemail@email.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'newuser',
        'email': 'newemail@email.com',
    }


def test_update_user_from_another_user(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user2',
            'email': 'user2@email.com',
            'password': 'password2',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'User not allowed to update this user'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_from_another_user(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'User not allowed to delete this user'
    }


def test_login_for_access_token(client, user):
    response = client.post(
        '/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'Bearer'


def test_login_for_access_token_invalid(client, user):
    response = client.post(
        '/token/',
        data={
            'username': 'wrong@test.com',
            'password': 'wrong',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
