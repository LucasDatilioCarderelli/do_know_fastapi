from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from do_know_fastapi.routers import auth, users
from do_know_fastapi.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
def read_root():
    return {'message': 'Olar World', 'extra': 'extra'}
