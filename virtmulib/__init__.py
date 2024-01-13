import os
import secrets
import dotenv 
import json

dotenv.load_dotenv()

os.environ['SESSION_ID'] = secrets.token_urlsafe(16)
