#!/usr/bin/env python

import requests

url = "http://localhost:8000/user/small"
file = {'f': open('upload.py', 'rb')}
resp = requests.post(url, files=file)
print (resp.json())
