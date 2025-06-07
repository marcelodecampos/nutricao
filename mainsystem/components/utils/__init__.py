#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""init file for utils module."""

from .base import base_layout
from .commom_layout import commom_layout
from .inputs import (
    birthdate_input,
    commom_label,
    common_birthdate_input,
    common_identification_input,
    common_input,
    common_name_input,
    common_nickname_input,
    email_input,
    identification_input,
    input_component,
    input_label_component,
    intersect,
    name_input,
    nickname_input,
    password_input,
)
from .simpletable.simple_table import simple_table_component
from .simpletable.simple_table_test import test_simple_table
from .user_info import user_info_options

__all__ = [
    "email_input",
    "password_input",
    "commom_layout",
    "commom_label",
    "common_input",
    "base_layout",
    "user_info_options",
    "common_name_input",
    "common_identification_input",
    "common_birthdate_input",
    "common_nickname_input",
    "simple_table_component",
    "test_simple_table",
    "input_label_component",
    "input_component",
    "intersect",
    "name_input",
    "identification_input",
    "birthdate_input",
    "nickname_input",
    "password_input",
]

__version__ = "0.1.0"
__author__ = "Marcelo de Campos"
