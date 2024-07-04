#!/usr/bin/env python

from data.init import conn
from sqlalchemy import MetaData, Table, Column, Text, insert, select
from service.user import get_hash, get_all, create
from model.user import User

def add_some_data():
    meta = MetaData()
    userTable = Table("users", meta,
            Column("name", Text, primary_key=True),
                  Column("hashpw", Text))

    #stmt = insert(userTable).values(name="shiva", hashpw=get_hash("shiva123"))
    #insert(userTable).values(name="soms", hashpw=get_hash("soms123"))
    #insert(userTable).values(name="jothi", hashpw=get_hash("jothi123"))

    #create(User(name='Dude', hash='whatever'))

    for u in get_all():
        print (u)

if __name__ == "__main__" :
    add_some_data()