from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool = False


class UserDB(BaseModel):
    password: str


users_db = {
    "jdoe": {
        "username": "jdoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
        "password": "123456",
    },
    "asmith": {
        "username": "asmith",
        "full_name": "Alice Smith",
        "email": "alicesmith@example.com",
        "disabled": True,
        "password": "123456",
    },
    "bwayne": {
        "username": "bwayne",
        "full_name": "Bruce Wayne",
        "email": "brucewayne@example.com",
        "disabled": False,
        "password": "123456",
    },
}


def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])
