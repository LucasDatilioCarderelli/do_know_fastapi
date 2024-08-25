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


def test_update_client(client, user):
    response = client.put(
        '/users/1',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'user2',
            'email': 'user2@email.com',
            'password': 'password2',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
