from pymongo import MongoClient
import User
import os
import sys
import bcrypt
import hashlib
import datetime

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
            "lastTime" : user.lastTime.strftime("%I:%M:%S"),
            "modemQuestionCompleted" : user.modemQuestionCompleted,
            "codeQuestionCompleted" : user.codeQuestionCompleted
    }

def userCustomDecode(document):
    assert document["_type"] == "user"
    time = document["lastTime"].split(":")
    return User.User(document["username"],
                    document["lastQuestionSubmitted"],
                    datetime.time(int(time[0]), int(time[1]), int(time[2])),
                    document["modemQuestionCompleted"],
                    document["codeQuestionCompleted"]
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
        data["lastTime"],
        False,
        False
    )

    new_user["user"] = userCustomEncode(new_user_object)
    
    new_user["token"] = data["token"]
    
    userAccts.insert_one(new_user)
    return 0


def get_time(token, currTime):
    ''' Gets the time from the last submission of the current user. '''

    new_token = hashlib.sha256(token.encode()).digest()
    user = userAccts.find_one({"token" : new_token}, {"_id" : 0})

    if user == None:
        return -1

    user = userCustomDecode(user["user"])

    timeFromLast = user.lastTime
    user.lastTime = currTime

    userAccts.update_one({"token" : new_token}, {"$set" : {"user" : userCustomEncode(user)}})

    return timeFromLast


def delete_user(token):

    new_token = hashlib.sha256(token.encode()).digest()
    userAccts.delete_one({"token" : new_token })


# Get and Set Lab Question Functions

def set_modem_true(token):

    new_token = hashlib.sha256(token.encode()).digest()

    user = userAccts.find_one({"token" : new_token})
    user = userCustomDecode(user["user"])
    user.modemQuestionCompleted = True

    userAccts.update_one({"token" : new_token}, {"$set" : {"user" : userCustomEncode(user)}})

    return


def check_modem_question(token):

    new_token = hashlib.sha256(token.encode()).digest()

    user = userAccts.find_one({"token" : new_token})
    user = userCustomDecode(user["user"])

    if user.modemQuestionCompleted:
        return True
    else:
        return False



# Get and Set Code Question Functions

def set_code_true(token):

    new_token = hashlib.sha256(token.encode()).digest()

    user = userAccts.find_one({"token" : new_token})
    user = userCustomDecode(user["user"])
    user.codeQuestionCompleted = True

    userAccts.update_one({"token" : new_token}, {"$set" : {"user" : userCustomEncode(user)}})

    return


def check_code_question(token):

    new_token = hashlib.sha256(token.encode()).digest()

    user = userAccts.find_one({"token" : new_token})
    user = userCustomDecode(user["user"])

    if user.codeQuestionCompleted:
        return True
    else:
        return False