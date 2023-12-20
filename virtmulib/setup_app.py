import os
import logging
import logging.config
import yaml
import json
from pythonjsonlogger import jsonlogger

#from .frameworks_drivers import CloudDB
from .frameworks_drivers.firebase import FirebaseDBLogger
from .entities import ProgState

import virtmulib.frameworks_drivers

logger = logging.getLogger(__name__)


class CloudLogHandler(logging.Handler):
    #This handler must always have a json formatter attached. See config/logging-*.yaml
    cdb = getattr(virtmulib.frameworks_drivers, 'FirebaseDBLogger')()
    
    def __init__(self)-> None:
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        path = f'logging/{os.environ["SESSION_ID"]}'
        self.cdb.push(self.format(record), path)
        

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


def fill_env_obj(obj):
    for key, value in obj.items():
        if type(value) is str:
            os.environ[key]=value
        elif type(value) is dict:
            fill_env_obj(value)
        elif type(value) is list:
            base_name=key[:-1]
            os.environ[base_name]=value[0]
            index = 2
            for item in value[1:]:
                os.environ[f'{base_name}{index}'] = item

def load_prog_state():
    db = FirebaseDBLogger()
    safe_ver = os.environ['VERSION'].replace('.', '')
    program_setup=db.get(f'program_state/{safe_ver}')[0]
    ps = ProgState(**program_setup).model_dump(exclude_defaults=True)
    fill_env_obj(ps)
    #os.environ['persist_user_lib']


def write_new_prog_state():
    db = FirebaseDBLogger()
    env = os.environ
    ver = env['VERSION']
    safe_ver = ver.replace('.', '')

    pr=ProgState(
        VERSION=ver,
        PERSIST_USER_LIB="yes",
        SPOTIFY_KEY={
                'SPOTIPY_CLIENT_ID': env['SPOTIPY_CLIENT_ID'],
                'SPOTIPY_CLIENT_SECRET': env['SPOTIPY_CLIENT_SECRET'],
                'SPOTIPY_REDIRECT_URI': env['SPOTIPY_REDIRECT_URI']},
        REPLICATE_KEYS=json.loads(env['REPLICATE_API_TOKENS']),
        END_OF_LIFE="no",
        WEBSITE="",
        LATEST_NEWS="",
        FEEDBACK_URL="")


    db.set(pr.model_dump(exclude_defaults=True), f'program_state/{safe_ver}')

