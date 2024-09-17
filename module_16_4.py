from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List

# Создаем объект FastAPI
app = FastAPI()

# Инициализация списка users
users = []

# Класс User, наследованный от BaseModel
class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос по маршруту '/users'
@app.get('/users', response_model=List[User])
async def get_users():
    return users

# POST запрос по маршруту '/user/{username}/{age}'
@app.post('/user/{username}/{age}', response_model=User)
async def add_user(
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    # Находим максимальный id
    max_id = max((user.id for user in users), default=0)
    new_id = max_id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос по маршруту '/user/{user_id}/{username}/{age}'
@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)],
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос по маршруту '/user/{user_id}'
@app.delete('/user/{user_id}', response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")