#from firebase_functions import logger

# Import the necessary modules

import firebase_admin
from firebase_admin import credentials, db

# Initialize the Firebase app with your project credentials
cred = credentials.Certificate('muski-6b55f-firebase-adminsdk-5ytkl-f0543d62e1.json')

s = firebase_admin.initialize_app(cred, {'databaseURL': 'https://muski-6b55f-default-rtdb.europe-west1.firebasedatabase.app/'})

#ref = db.reference()

ref = db.reference('logging')

print(dir(s))

# data = ref.get()
# print(data)

# "https://muski-6b55f-default-rtdb.europe-west1.firebasedatabase.app/"

