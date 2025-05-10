# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""init module for mixin aux class component."""

import json
from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, String, BigInteger, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql import func

DEFAULT_NAME_FIELD_SIZE = 256
# pylint: disable=missing-class-docstring


class InsertDateMixin:
    time_created: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        sort_order=98,
    )


class UpdateDateMixin:
    time_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),  # pylint: disable=not-callable
        sort_order=99,
    )


class NameMixin:
    name: Mapped[str] = mapped_column(String(DEFAULT_NAME_FIELD_SIZE), nullable=False, sort_order=2)

    @validates("name")
    def validate_name(self, key, field: str) -> str:
        """Should we make it uppercase????"""
        if field:
            return field.upper().strip()
        raise ValueError("Name could not be null")

    def __str__(self):
        return f"Name(name={self.name}, {super().__str__()}"


class IsValidMixin:
    """IsValid mixin class"""

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="t",
        sort_order=97,
    )


class InsertUpdateDateMixin(InsertDateMixin, UpdateDateMixin): ...
