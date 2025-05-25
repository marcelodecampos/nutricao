#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""init file for utils module."""

from .email import email_input
from .password import password_input
from .commom_layout import commom_layout
from .base import base_layout
from .user_info import user_info_options
from .inputs import (
    common_name_input,
    common_identification_input,
    common_birthdate_input,
    common_nickname_input,
)

__all__ = [
    "email_input",
    "password_input",
    "commom_layout",
    "base_layout",
    "user_info_options",
    "common_name_input",
    "common_identification_input",
    "common_birthdate_input",
    "common_nickname_input",
]

__version__ = "0.1.0"
__author__ = "Marcelo de Campos"
