from sqlalchemy import select

from do_know_fastapi.models import User


def test_create_user(session):
    user = User(username='user', password='password', email='user@email.com')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.id == 1))

    assert result.id == 1
    assert result.username == 'user'
