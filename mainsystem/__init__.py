#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, missing-class-docstring, missing-function-docstring
"""init module form application"""

import logging
import logging.handlers
import sys
import os
from .app_state import AppState


# just in case
sys.path.append(os.getcwd())


__version__ = "0.1.0"
__author__ = "Marcelo de Campos"


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    str_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + str_format + reset,
        logging.INFO: grey + str_format + reset,
        logging.WARNING: yellow + str_format + reset,
        logging.ERROR: red + str_format + reset,
        logging.CRITICAL: bold_red + str_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_logger():
    logger = logging.getLogger()  # root logger
    env_log_name = "LOGLEVEL"
    log_level = os.environ.get(env_log_name, "DEBUG").upper()
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(CustomFormatter())
    # logger.addHandler(stream_handler)
    log_file_path = os.environ.get("LOG_TO_FILE", None)
    if log_file_path:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(CustomFormatter.str_format))
        logger.addHandler(file_handler)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
    logger.debug("The logger is configured")


configure_logger()


__all__ = [
    "AppState",
    "configure_logger",
    "__version__",
    "__author__",
]
