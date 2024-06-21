#!/usr/bin/env python

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from web import user

from model.user import User

app = FastAPI()
app.include_router(user.router)

#basic: HTTPBasicCredentials = HTTPBasicCredentials()
#pwd: str = "mypass"
#uname: str = "myuser"

#@app.get("/who")
#def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> User:
#    if creds.username == uname and creds.password == pwd:
#        return User(name=uname, hash=pwd)
#    raise HTTPException(status_code=401, detail="Invalid Login")
##

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
