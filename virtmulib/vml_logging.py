import os
import logging
import logging.config
import yaml
from pythonjsonlogger import jsonlogger


#from .frameworks_drivers import CloudDB
import virtmulib.frameworks_drivers

logger = logging.getLogger(__name__)


class CloudLogHandler(logging.Handler):
    cdb = getattr(virtmulib.frameworks_drivers, 'FirebaseDBLogger')()
    
    def __init__(self)-> None:
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        self.cdb.create(self.format(record))


def json_logger_fact(format):
    return jsonlogger.JsonFormatter(
            format,
            rename_fields={"levelname": "log_level", "asctime": "timestamp"}
        )

def setup_logging_env():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.yaml", "prod": "logging.prog.yaml"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.yaml")
    config_path = os.path.join(os.environ["CONFIG_DIR"], config)

    with open(config_path, 'r') as file:
        logging.config.dictConfig(yaml.safe_load(file))
    
    #logging.getLogger("nose").propagate = True
    #logging.getLogger().addHandler(CloudLogHandler)
    #logging.getLogger().setLevel(logging.DEBUG)
