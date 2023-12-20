import os
import secrets
import dotenv 

dotenv.load_dotenv()

os.environ['SESSION_ID'] = secrets.token_urlsafe(16)

