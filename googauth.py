#!/usr/bin/env python
import os

from fastapi import FastAPI, Depends
from fastapi.responses import  RedirectResponse
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
import json

from dotenv import load_dotenv

import service.user as service
load_dotenv("./.env")


## Example Google Social Login ..

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google"

@app.get("/login/google")
async def login_google():
    url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return RedirectResponse(url)

@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_json = json.loads(user_info.content)

    access_token = service.create_access_token(data={"sub": user_json['email']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, service.SECRET_KEY, algorithms=["HS256"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)