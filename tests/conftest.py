import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from do_know_fastapi.app import app
from do_know_fastapi.database import get_session
from do_know_fastapi.models import User, table_registry
from do_know_fastapi.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'password'
    user = User(
        username='user', email='user@test.com', password=get_password_hash(pwd)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patching

    return user


@pytest.fixture
def users(session):
    users = [
        User(username='user1', email='user1@test.com', password='password'),
        User(username='user2', email='user2@test.com', password='password'),
        User(username='user3', email='user3@test.com', password='password'),
    ]

    session.add_all(users)
    session.commit()
    session.refresh(users[0])
    session.refresh(users[1])
    session.refresh(users[2])

    return users


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
