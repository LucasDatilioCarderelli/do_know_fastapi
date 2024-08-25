from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from do_know_fastapi.schemas import (
    ListUserPublicSchema,
    Message,
    UserDBSchema,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
def read_root():
    return {'message': 'Olar World', 'extra': 'extra'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema):
    user_with_id = UserDBSchema(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=ListUserPublicSchema,
)
def read_user():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDBSchema(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    database.pop(user_id - 1)
    return {'message': 'User deleted'}
