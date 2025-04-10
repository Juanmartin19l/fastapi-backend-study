from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"theme": "dark"})


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [
    User(id=1, name="Juan", surname="Lavalle", age=22),
    User(id=2, name="Pepe", surname="Pip", age=34),
    User(id=3, name="ella", surname="El", age=55),
    User(id=4, name="Ramon", surname="Taro", age=98),
]


# GET ALL USERS BY ID
@app.get("/users")
async def get_users():
    return users_list


# GET
@app.get("/user/{id}")
async def get_user(id: int):
    return search_user(id)


# GET
@app.get("/user/")
async def get_user_query(id: int):
    return search_user(id)


# POST
@app.post("/user/", status_code=201)
async def post_user(user: User):
    if type(search_user(user.id)) == User:  # noqa: E721
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user


# PUT
@app.put("/user/")
async def put_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    return user


# DELETE
@app.delete("/user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha borrado el usuario"}
    return {"se ha borrado el usuario"}


# Search user
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "not found"}
