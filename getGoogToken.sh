#!/bin/sh

curl -v -X GET -H "Authorization:  \
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGl2YS5qYXlhcmFtYW5AZ21haWwuY29tIiwiZXhwIjoxNzE4OTU2MDAyfQ.NHeyCXW93KrmCkcgbCIPLbr3cj4kj6PLGkVn_pblYS0" \
http://localhost:8000/token

