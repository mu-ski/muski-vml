import os
import logging

from . import vml_logging
from .frameworks_drivers.firebase import FirebaseDBLogger

user_logger = FirebaseDBLogger()

if __name__ == '__main__':

    vml_logging.setup_logging_env()


    logger = logging.getLogger(__name__)
    
    logger.info("Program started")

    logger.info("Program finished")

    user_logger.create({'username': {'session_id': os.environ['SESSION_ID']}})