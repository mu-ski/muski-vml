import logging
import os
from datetime import datetime
from dotenv import dotenv_values

# load env variables into CONFIG without touching the environment
CONFIG = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}


if __name__ == '__main__':
    setup_logging()

    logger = logging.getLogger(__name__)
    
    logger.info("Program started")
