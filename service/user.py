from datetime import timedelta, datetime
import os
from jose import jwt
from  model.user import User

from data import user as data

from passlib.context import CryptContext

SECRET_KEY = "my-secret"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain: str, hash:str) ->bool :
    return pwd_context.verify(plain, hash)

def get_hash(plain:str) -> str:
    return pwd_context.hash(plain)

def get_jwt_username(token: str) -> str | None:
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub"))  :
            return None
    except jwt.JWTError:
        return None
    return username

def get_current_user(token: str) ->User |None:
    if not (username := get_jwt_username(token)) :
        return None
    if user := lookup_user(username) :
        return user
    return

def lookup_user(username: str) -> User:
    if (user := data.get_one(username)) :
        return user
    return None

def auth_user(name: str, plain: str) -> User|None:
    if not (user := lookup_user(name)) :
        return None
    if not verify_password(plain, user.hash) :
        return None
    return user

def create_access_token(data: dict, expires: timedelta|None = None):
    src = data.copy()
    now = datetime.utcnow()
    if not expires :
        expires = timedelta(minutes=15)
    src.update({"exp" : now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_all() -> list[User] :
    users: list[User] = data.get_all()
    print (users)
    return users;


def get_one(name) -> User :
    return data.get_one(name)

def create(user: User) -> User:
    user.hash = get_hash(user.hash)
    return data.create(user)

def modify(name: str, user: User) ->User:
    return data.modify(name, user)

def delete(name: str) -> None:
    return data.delete(name)






