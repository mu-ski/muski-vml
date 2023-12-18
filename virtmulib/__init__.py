import os
import logging
from datetime import datetime
from dotenv import dotenv_values

# load env variables into CONFIG without touching the environment
CONFIG = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
