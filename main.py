from fastapi import FastAPI
from sqlmodel import SQLModel


class User(SQLModel):
    id:int 
    username: str
    hashed_password: str
    email: str
    is_active: bool = True

class UserLogin(SQLModel):
    username: str
    password: str

class UserCreate(SQLModel):
    username: str
    password: str
    email: str

class UserRead(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool

class UserUpdate(SQLModel):
    username: str
    email: str
    is_active: bool

class LoginRequest(SQLModel):
    username: str
    password: str


app = FastAPI()


users_db = {
    "admin": UserLogin(username="admin", password="1234"),
}

@app.post("/Users")
def create_user(user: UserCreate):
    if user.username in users_db:
        return {"message": "Username already exists."}
    users_db[user.username] = UserLogin(username=user.username, password=user.password)
    return {"message": "User created successfully."}


@app.get("/Users")
def read_users(user: UserCreate):
    return list(users_db.values())



@app.get("/Users/{user_id}")
def read_user(user_id: int):
    user_list = list(users_db.values())
    if 0 <= user_id < len(user_list):
        return user_list[user_id]
    return {"message": "User not found."}



@app.put("/Users/{user_id}")
def update_user(user_id: int, user_update: UserCreate):
    user_list = list(users_db.values())
    if 0 <= user_id < len(user_list):
        users_db[user_update.username] = UserLogin(username=user_update.username, password=user_update.password)
        return {"message": "User updated successfully."}
    return {"message": "User not found."}



@app.delete("/Users/{user_id}")
def delete_user(user_id: int):
    user_list = list(users_db.values())
    if 0 <= user_id < len(user_list):
        del users_db[user_list[user_id].username]
        return {"message": "User deleted successfully."}
    return {"message": "User not found."}


@app.post("/login")
def login(user: UserLogin):
    for username, db_user in users_db.items():
        if db_user.username == user.username and db_user.password == user.password:
            return {"message": "Aleluya"}
    
    return {"message": "usuario y/o contraseña incorrectos."}


