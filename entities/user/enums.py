#!  python3
# -*- coding: utf-8 -*-
"""Module File"""

from enum import Enum, unique, IntEnum


@unique
class ContDocID(IntEnum):
    """Contact Document Enum Types"""

    (
        CPF,
        PASSPORT,
        IDENTITY,
        PIS_PASEP,
        VOTER_ID,
        BIRTH_CERTIFICATE,
        CNPJ,
        CELL_PHONE,
        PHONE,
        EMAIL,
    ) = range(1, 11)


@unique
class PersonType(Enum):
    """Enum Person Types"""

    PERSON = "F"
    COMPANY = "J"
