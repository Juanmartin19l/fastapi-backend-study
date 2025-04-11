from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Users"])


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


# GET ALL USERS
@router.get("/users")
async def get_users():
    return users_list


# GET BY ID
@router.get("/user/{id}")
async def get_user(id: int):
    user = search_user(id)
    if not isinstance(user, User):
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {id} no encontrado"
        )
    return user


# GET BY ID Query
@router.get("/user/")
async def get_user_query(id: int):
    user = search_user(id)
    if not isinstance(user, User):
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {id} no encontrado"
        )
    return user


# POST
@router.post("/user/", status_code=201)
async def post_user(user: User):
    if isinstance(search_user(user.id), User):
        raise HTTPException(
            status_code=400, detail=f"El usuario con id {user.id} ya existe"
        )
    users_list.append(user)
    return user


# PUT
@router.put("/user/")
async def put_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            break
    if not found:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {user.id} no encontrado"
        )
    return {"actualizado": user}


# DELETE
@router.delete("/user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            break
    if not found:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {id} no encontrado"
        )
    return {"message": f"Se ha borrado el usuario con id: {id}"}


# Search user
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return None
