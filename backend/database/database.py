from pymongo import MongoClient
import User
import exceptions
import os
import sys
import bcrypt
import hashlib

# Initialize the Mongo connection here
mongoClient = MongoClient('mongo')
db = mongoClient("Jenn's Research")

# Initialize all collections here
userAccts = db["userAccts"]

theSalt = bcrypt.gensalt()