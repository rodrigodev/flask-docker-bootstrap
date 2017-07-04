#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from .config import USERS_COLLECTION


def main():
    pass_hash = generate_password_hash("tada123", method='pbkdf2:sha256')
    try:
        USERS_COLLECTION.insert({"_id": "tada", "password": pass_hash})
        print("User created.")
    except DuplicateKeyError:
        print("User already present in DB.")


if __name__ == '__main__':
    main()
