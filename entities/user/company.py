#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument, logging-fstring-interpolation, unsubscriptable-object)
"""Module File"""

import re
from typing import Optional

from sqlalchemy import ForeignKey, Relationship, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..base import SimpleTable
from .constants import CNPJ_SIZE
from .enums import PersonType
from .user import User


class CompanySize(SimpleTable):
    """Base class for Company Size"""

    __tablename__ = "company_size"
    short_name: Mapped[str] = mapped_column(String(12), nullable=False, sort_order=3)

    def __str__(self):
        return f"CompanySize(short_name={self.short_name})"


class EconimicActivitySection(SimpleTable):
    """Base class for Economic Activity Section"""

    __tablename__ = "economic_activity_section"
    code: Mapped[str] = mapped_column(
        String(8), nullable=False, unique=True, sort_order=3
    )

    def __str__(self):
        return f"EconimicActivitySection(code={self.code}, description={self.name})"


class EconimicActivityDivision(SimpleTable):
    """Base class for Economic Activity Division"""

    __tablename__ = "economic_activity_division"
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("economic_activity_section.id"),
        nullable=False,
        sort_order=2,
    )
    code: Mapped[str] = mapped_column(
        String(8), nullable=False, unique=True, sort_order=3
    )
    parent: Mapped[Optional[EconimicActivitySection]] = Relationship()

    def __str__(self):
        return f"EconimicActivityDivision(code={self.code}, description={self.name})"


class EconimicActivityGroup(SimpleTable):
    """Base class for Economic Activity Group"""

    __tablename__ = "economic_activity_group"
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("economic_activity_division.id"),
        nullable=False,
        sort_order=2,
    )
    code: Mapped[str] = mapped_column(
        String(8), nullable=False, unique=True, sort_order=3
    )
    parent: Mapped[Optional[EconimicActivityDivision]] = Relationship()

    def __str__(self):
        return f"EconimicActivityGroup(code={self.code}, description={self.name})"


class EconimicActivityClass(SimpleTable):
    """Base class for Economic Activity Class"""

    __tablename__ = "economic_activity_class"
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("economic_activity_group.id"),
        nullable=False,
        sort_order=2,
    )
    code: Mapped[str] = mapped_column(
        String(16), nullable=False, unique=True, sort_order=3
    )
    parent: Mapped[Optional[EconimicActivityGroup]] = Relationship()

    def __str__(self):
        return f"EconimicActivityClass(code={self.code}, description={self.name})"


class EconimicActivity(SimpleTable):
    """Base class for Economic Activity"""

    __tablename__ = "economic_activity"
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("economic_activity_class.id"),
        nullable=False,
        sort_order=2,
    )
    code: Mapped[str] = mapped_column(
        String(16), nullable=False, unique=True, sort_order=3
    )
    parent: Mapped[Optional[EconimicActivityClass]] = Relationship()

    def __str__(self):
        return f"EconimicActivity(code={self.code}, description={self.name})"


class Company(User):
    """Base class Company"""

    __tablename__ = "company"
    __mapper_args__ = {
        "polymorphic_identity": PersonType.COMPANY.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True, sort_order=3
    )
    cnpj: Mapped[Optional[str]] = mapped_column(
        String(CNPJ_SIZE),
        nullable=True,
        unique=True,
        sort_order=4,
    )
    size_id: Mapped[int] = mapped_column(
        ForeignKey("company_size.id"),
        nullable=False,
        sort_order=5,
        default=1,
        server_default="1",
        default_factory=lambda: 1,
    )

    size: Mapped[Optional[CompanySize]] = Relationship()

    @validates("cnpj")
    def validate_cnpj(self, key, field: str) -> str:
        """validate CPF"""
        if field:
            field = re.sub(r"\D", "", field).zfill(CNPJ_SIZE)
            return field
        raise ValueError("CNPJ could not be null")
