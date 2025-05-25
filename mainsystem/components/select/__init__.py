#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable

import logging
from .base import common_select_component, get_values_from_database
from .title import title_options
from .gender import gender_options
from .marital_status import marital_status_options
from .education import education_options


__version__ = "0.1.0"
__author__ = "Marcelo de Campos"


__all__ = [
    "title_options",
    "gender_options",
    "marital_status_options",
    "education_options",
    "common_select_component",
    "get_values_from_database",
]
