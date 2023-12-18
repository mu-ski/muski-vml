#from firebase_functions import logger

# Import the necessary modules

import os
import firebase_admin
from firebase_admin import credentials, db

from .interface  import CloudDB

firebase_admin.initialize_app(
    credentials.Certificate(
        os.environ['FIREBASE_JSON_KEY_PATH']), 
        {'databaseURL': os.environ['FIREBASE_DB_URL']})

ref = db.reference("logging")

#logger = logging.getLogger(__name__)


class FirebaseDBLogger(CloudDB):
    def create(self, item: dict):
        ref.set(item)
        pass

    def read(self, item: dict):
        pass

    def update(self, item: dict):
        pass

    def delete(self, item: dict):
        pass


# # Initialize the Firebase app with your project credentials

# cred = credentials.Certificate(os.environ['FIREBASE_JSON_KEY_PATH'])
# conn = firebase_admin.initialize_app(
#                                 credentials.Certificate(
#                                     os.environ['FIREBASE_JSON_KEY_PATH']), 
#                                     {'databaseURL': os.environ['FIREBASE_DB_URL']}
#                                 )
# print(type(conn) is firebase_admin.App)
#ref = db.reference()

#ref = db.reference('logging').set({'act': 2})

#print(s)

# data = ref.get()
# print(data)

# "https://muski-6b55f-default-rtdb.europe-west1.firebasedatabase.app/"

