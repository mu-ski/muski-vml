import logging

from . import vml_logging



if __name__ == '__main__':

    vml_logging.setup_logging_env()    

    logger = logging.getLogger(__name__)

    logger.info("Program started")
