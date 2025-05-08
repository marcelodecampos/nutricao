#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument)
"""Module File"""

from typing import Optional
from datetime import date

from sqlalchemy import (
    String,
    CHAR,
    Date,
    ForeignKey,
    Boolean,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlmodel import Relationship

from .base import Base, Name, SimpleTable, DEFAULT_NAME_FIELD_SIZE
from .person import Person, Company


class Role(SimpleTable):
    """Access Role Simple Table"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "role"


class Permission(SimpleTable):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "permission"


class Resource(SimpleTable):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "resource"
    url: Mapped[str] = mapped_column(String(DEFAULT_NAME_FIELD_SIZE), nullable=False, sort_order=3)
