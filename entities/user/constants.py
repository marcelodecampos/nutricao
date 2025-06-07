#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=pointless-string-statement
"""this is the init module for entities module"""

from sqlalchemy import CheckConstraint

TYPE_PERSON_CHECK_CONSTRAINT = CheckConstraint("person_type IN ('F', 'J', NULL)")
CONTDOC_CHECK_CONSTRAINT = CheckConstraint("contdoc_type IN ('C', 'D')")
CPF_SIZE = 11
CNPJ_SIZE = 14
STOP_CHARS = r"\D+"
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
DEFAULT_NAME_FIELD_SIZE = 256
