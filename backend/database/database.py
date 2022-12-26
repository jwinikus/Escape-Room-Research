from pymongo import MongoClient
import User
import os
import sys
import bcrypt
import hashlib
from datetime import datetime

# Initialize the Mongo connection here
mongoClient = MongoClient('mongo')
db = mongoClient["Jenn's_Research"]

# Initialize all collections here
userAccts = db["userAccts"]


# Encoding and Decoding User Custom Classes
def userCustomEncode(user):
    return {"_type": "user", 
            "username" : user.username,
            "lastQuestionSubmitted" : user.lastQuestionSubmitted,
            "lastTime" : user.lastTime.strftime("%I:%M:%S")
    }

def userCustomDecode(document):
    assert document["_type"] == "user"
    time = document["lastTime"].split(":")
    return User.User(document["username"],
                    document["lastQuestionSubmitted"],
                    datetime.time(time[0], time[1], time[2])
    )
    
    
def insert_data(data):
    '''insert data to collections userAccts'''

    all_users = userAccts.find({})
    if data["username"] in all_users:
        return -1

    new_user = {}
    new_user["username"] = data["username"]
    

    new_user_object = User.User(
        data["username"],
        data["lastQuestionSubmitted"],
        data["lastTime"]
    )

    new_user["user"] = userCustomEncode(new_user_object)
    
    new_user["token"] = data["token"]
    
    userAccts.insert_one(new_user)
    return 0