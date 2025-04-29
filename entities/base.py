#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument)
"""module file"""

import json
from datetime import datetime
from typing import Optional
from functools import total_ordering
from sqlalchemy import DateTime, Integer, String, Boolean, BigInteger, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.sql import func

from utils.logger import get_logger

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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, sort_order=1)

    def __str__(self):
        return f"User(id={self.id})"

    def __eq__(self, other: any):
        if not other:
            return False
        if isinstance(other, SerialID):
            return self.id == other.id
        if isinstance(other, (int | Integer | BigInteger)):
            return self.id == other
        return False

    def __lt__(self, other: any):
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


class InsertDate:
    """Abstract class to implement an insert date and update date on almost every table"""

    time_created: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        sort_order=98,
    )


class InsertUpdateDate(InsertDate, Base):
    """Abstract class to implement an insert date and update date on almost every table"""

    __abstract__ = True
    time_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),  # pylint: disable=not-callable
        sort_order=99,
    )


class Name(SerialID, InsertUpdateDate):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True
    name: Mapped[str] = mapped_column(String(DEFAULT_NAME_FIELD_SIZE), nullable=False, sort_order=2)

    @validates("name")
    def validate_name(self, key, field: str) -> str:
        """Should we make it uppercase????"""
        if field:
            return field.upper().strip()
        raise ValueError("Name could not be null")

    def __str__(self):
        return f"Name(name={self.name}, {super().__str__()}"


class UniqName(Name):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True
    __table_args__ = (UniqueConstraint("name"),)


class SimpleTable(UniqName):
    """Abstract class to implement a name on almost every table"""

    __abstract__ = True
    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="t",
        sort_order=97,
    )

    def __str__(self):
        return super().__str__() + f", 'isvalid': {self.is_valid}"
