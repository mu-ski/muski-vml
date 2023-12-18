import logging.config
import logging
from pathlib import Path
import yaml
from pythonjsonlogger import jsonlogger
from firebase_admin import credentials, db
import firebase_admin

from . import CONFIG

logger = logging.getLogger(__name__)


class CloudLogHandler(logging.Handler):
    def __init__(self)-> None:
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        # TODO: add call to firebase
        print(f'jhaha {self.format(record)}')


def json_logger_fact(format):
    return jsonlogger.JsonFormatter(
            format,
            rename_fields={"levelname": "log_level", "asctime": "timestamp"}
        )

def setup_logging_env():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.yaml", "prod": "logging.prog.yaml"}
    config = log_configs.get(CONFIG["ENV"], "logging.dev.yaml")
    config_path = Path(CONFIG['CONFIG_DIR']).joinpath(config)

    Path(CONFIG['LOG_DIR']).mkdir(parents=True, exist_ok=True)

    with open(config_path, 'r') as file:
        logging.config.dictConfig(yaml.safe_load(file))


