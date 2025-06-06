#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument)
"""module file"""

import json
from datetime import datetime
from functools import total_ordering
from typing import Self

from sqlalchemy import BigInteger, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from utils.logger import get_logger

from .mixin import InsertUpdateDateMixin, IsValidMixin, ValidateNameMixin

# Create a PostgreSQL database engine
# Define a model for your users
DEFAULT_NAME_FIELD_SIZE = 256
LOGGER = get_logger("state")


# declarative base class
class Base(DeclarativeBase):
    """base class for all"""

    __abstract__ = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for key, value in kwargs.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)


@total_ordering
class SerialID(Base):
    """Abstract class to implement a serial id on almost every table"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, sort_order=1
    )

    def __str__(self):
        return f"User(id={self.id})"

    def __eq__(self, other: object | int | Integer | BigInteger):
        if not other:
            return False
        if isinstance(other, SerialID):
            return self.id == other.id
        if isinstance(other, (int | Integer | BigInteger)):
            return self.id == other
        return False

    def __lt__(self, other: Self | int | Integer | BigInteger):
        if not other:
            return False
        if isinstance(other, SerialID):
            return self.id < other.id
        if isinstance(other, (int | Integer | BigInteger)):
            return self.id < other
        return False

    def __repr__(self):
        dict_repr = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in dict_repr.items():
            if isinstance(value, datetime):
                dict_repr[key] = datetime.isoformat(value)
        return json.dumps(dict_repr, indent=2)


class Name(SerialID, InsertUpdateDateMixin, ValidateNameMixin):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True
    name: Mapped[str] = mapped_column(
        String(DEFAULT_NAME_FIELD_SIZE), nullable=False, sort_order=2
    )

    def __str__(self):
        return f"Name(name={self.name}, {super().__str__()}"


class UniqueNameMixin:
    """Abstract class to implement a name on almost every table"""

    __table_args__ = (UniqueConstraint("name"),)


class UniqName(UniqueNameMixin, Name):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True


class SimpleTable(IsValidMixin, UniqName):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True

    def __str__(self):
        return super().__str__() + f", 'isvalid': {self.is_valid}"
