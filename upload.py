#!/usr/bin/env python

## Can do this from the command line too
## http -f -b http://localhost:8000/small f@upload.py

import requests


url = "http://localhost:8000/user/small"
file = {'f': open('upload.py', 'rb')}
resp = requests.post(url, files=file)
print (resp.json())
