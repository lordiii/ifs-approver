import logging
from os.path import join

# https://docs.python.org/2/howto/logging.html
from ifsApprover import config
from ifsApprover.Utils import make_dirs_if_needed


def get_logger(name):
    return logging.getLogger("ifs.%s" % name)


def init_logger():
    _configure_logger('ifs', "ifs")
    _configure_logger('web')


def _configure_logger(file_name, logger_name=None):
    level = logging.DEBUG
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    if logger_name is not None:
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
