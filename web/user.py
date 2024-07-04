import os
from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import  User
from service import user as service

from errors import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(prefix = "/user") # --- new auth stuff

# This dependency makes a post to "/user/token"
# (from a form containing a username and password) # and returns an access token.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="/user/token")

def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
        )

# This endpoint is directed to by any call that has the # oauth2_dep() dependency:
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm =  Depends()):
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.name}, expires=expires )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token} # --- previous CRUD stuff

@router.get("/")
#def get_all(token: str = Depends(oauth2_dep)) -> list[User]:
def get_all() -> list[User]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


from fastapi import File
@router.post("/small")
async def upload_small_file(f : bytes = File()) -> str :
    return f"file size : {len(f)}"
