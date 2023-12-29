import os
import secrets
import dotenv 
import json

dotenv.load_dotenv()

os.environ['SESSION_ID'] = secrets.token_urlsafe(16)
os.environ['REPLICATE_API_TOKEN']=json.loads(os.environ['REPLICATE_API_TOKENS'])[0]
