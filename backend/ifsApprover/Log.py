import logging
import os
from os.path import join


# https://docs.python.org/2/howto/logging.html
from ifsApprover import config
from ifsApprover.Utils import make_dirs_if_needed


def get_logger(name):
    return logging.getLogger("ifs.%s" % name)


def init_wsgi_logger():
    _configure_logger('wsgi-ifs', "ifs")
    _configure_logger('wsgi-web')


def init_cli_logger():
    _configure_logger('cli')


def _configure_logger(file_name, logger_name=None):
    level = logging.DEBUG
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    if not logger_name is None:
        logger.propagate = False

    file_path = join(config["LOG_DIR"], "%s.log" % file_name)
    make_dirs_if_needed(file_path)
    fh = logging.FileHandler(file_path)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if config["CONSOLE_LOGGING"]:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
