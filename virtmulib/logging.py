import logging.config
import logging
import yaml


# with open('./config/logging.prog.yaml', 'r') as file:
#     conf = yaml.safe_load(file)


def setup_logging_env():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(CONFIG["ENV"], "logging.dev.ini")
    config_path = "/".join([CONFIG['CONFIG_DIR'], config])

    timestamp = datetime.now().strftime("%Y%m%d-%H_%M_%S")

    import pathlib
    pathlib.Path(CONFIG['LOG_DIR']).mkdir(parents=True, exist_ok=True)

    CONFIG['LOG_DIR']

    #JsonFormatter()
    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{CONFIG['LOG_DIR']}/{timestamp}.log"},
    )
