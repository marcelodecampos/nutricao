#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, missing-class-docstring, missing-function-docstring
"""init module form application"""

import logging
import sys
import os


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
    logger.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
    # stream_handler.setFormatter(CustomFormatter())

    # logger.addHandler(stream_handler)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
    logger.debug("The logger is configured")


configure_logger()
