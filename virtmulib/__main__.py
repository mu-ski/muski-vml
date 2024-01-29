import logging

# from .frameworks_drivers import CloudDB
from . import setup_app
import virtmulib.applogic.program_flow as program_flow


if __name__ == "__main__":
    setup_app.setup_logging_env()

    logger = logging.getLogger(__name__)

    # setup_app.write_new_prog_state()
    setup_app.load_prog_state()

    # logger.info("Program started")

    program_flow.prog_logic()

    # logger.info("Program finished")
