#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument)
"""Module File"""

import reflex as rx
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import (
    SimpleTable,
    SimpleTableModel,
)

from .base import DEFAULT_NAME_FIELD_SIZE


class RoleModel(SimpleTableModel, rx.Model):
    """Access Role Simple Table"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "role"


class Role(SimpleTable):
    """Access Role Simple Table"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "role"


class PermissionModel(SimpleTableModel, rx.Model):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "permission"


class Permission(SimpleTable):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "permission"


class ResourceModel(SimpleTableModel, rx.Model):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "resource"

    url: str


class Resource(SimpleTable):
    """Permission Role"""

    __table_args__ = {"schema": "access"}
    __tablename__ = "resource"
    url: Mapped[str] = mapped_column(String(DEFAULT_NAME_FIELD_SIZE), nullable=False, sort_order=3)
