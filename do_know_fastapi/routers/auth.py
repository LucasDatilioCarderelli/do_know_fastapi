from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from do_know_fastapi.database import get_session
from do_know_fastapi.models import User
from do_know_fastapi.schemas import TokenSchema
from do_know_fastapi.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuthToken = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token/', status_code=HTTPStatus.OK, response_model=TokenSchema)
def login_for_access_token(session: T_Session, form_data: T_OAuthToken):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    acces_token = create_access_token(data={'sub': user.email})

    return {'access_token': acces_token, 'token_type': 'Bearer'}
