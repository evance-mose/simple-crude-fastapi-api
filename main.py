from http.client import HTTPException
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI

from models import Gender, Role, User, UserUpdate

app = FastAPI()


db: List[User] = [
    User(
        id=UUID("54d6016c-2013-4291-99dc-4971ced85cf7"),
        first_name="John",
        last_name="Doe",
        middle_name="Thomas",
        gender=Gender.male,
        roles=[Role.user]
    ),
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return {
        "id": user.id,
        "message": "User created successfully"
    }


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {
                "id": user_id,
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} not found"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdate):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return {
                "id": user_id,
                "message": "User updated successfully"
            }
    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} not found"
    )
