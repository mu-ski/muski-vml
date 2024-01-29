# from firebase_functions import logger

# Import the necessary modules

import os
import firebase_admin
from firebase_admin import credentials, db

from .interface import CloudDB


# ref = db.reference("logging")
# ref2 = ref.child("-Nm0PR4gi16KWmhXMgZq")
# print(ref2.get())


# logger = logging.getLogger(__name__)
# app = firebase_admin.initialize_app(
#         credentials.Certificate(os.environ['FIREBASE_JSON_KEY_PATH']),
#         {'databaseURL': os.environ['FIREBASE_DB_URL']})

firebase_admin.initialize_app(
    credentials.Certificate(os.environ["FIREBASE_JSON_KEY_PATH"]),
    {"databaseURL": os.environ["FIREBASE_DB_URL"]},
)


class FirebaseDBLogger(CloudDB):
    def set(self, item: dict, path):
        return db.reference(path).set(item)

    def push(self, item: dict, path):
        return db.reference(path).push(item)

    def get(self, path):
        return db.reference(path).get(path)

    def update(self, item: dict, path):
        db.reference(path).update(item)
        pass

    def delete(self, path):
        db.reference(path).delete()
        pass


# # Initialize the Firebase app with your project credentials

# cred = credentials.Certificate(os.environ['FIREBASE_JSON_KEY_PATH'])
# conn = firebase_admin.initialize_app(
#                                 credentials.Certificate(
#                                     os.environ['FIREBASE_JSON_KEY_PATH']),
#                                     {'databaseURL': os.environ['FIREBASE_DB_URL']}
#                                 )
# print(type(conn) is firebase_admin.App)
# ref = db.reference()

# ref = db.reference('logging').set({'act': 2})

# print(s)

# data = ref.get()
# print(data)

# "https://muski-6b55f-default-rtdb.europe-west1.firebasedatabase.app/"
