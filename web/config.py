import os
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'put_your_secret_key_here'

DB_NAME = 'tada'

DATABASE = MongoClient("mongodb://mongodb:27017".format(DB_USER, DB_PASS))[DB_NAME]
TODO_COLLECTION = DATABASE.todos
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True
