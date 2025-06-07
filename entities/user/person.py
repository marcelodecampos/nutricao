#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument, logging-fstring-interpolation)
"""Module File"""

import logging
import re
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..base import Name, SimpleTable
from .constants import CPF_SIZE
from .enums import PersonType
from .user import User

LOGGER = logging.getLogger(__name__)


class MaritalStatus(SimpleTable):
    """Base class User"""

    __tablename__ = "marital_status"


class Gender(SimpleTable):
    """Base class User"""

    __tablename__ = "gender"


class Education(SimpleTable):
    """Base class User"""

    __tablename__ = "education"


class Title(Name):
    """Title class table"""

    __tablename__ = "title"
    gender_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("gender.id"), nullable=True, sort_order=3
    )
    shortening: Mapped[str] = mapped_column(String(32), sort_order=4)
    gender: Mapped[Optional[Gender]] = relationship(lazy="immediate")
    __table_args__ = (UniqueConstraint("name", "gender_id"),)


class Person(User):
    """Base class Person"""

    __logger = logging.getLogger(__name__)
    __tablename__ = "person"
    __mapper_args__ = {
        "polymorphic_identity": PersonType.PERSON.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), sort_order=1, primary_key=True
    )
    cpf: Mapped[Optional[str]] = mapped_column(
        String(CPF_SIZE),
        nullable=True,
        unique=True,
        sort_order=4,
    )
    gender_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("gender.id"), sort_order=5, nullable=True
    )
    title_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("title.id"), nullable=True, sort_order=6
    )
    marital_status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("marital_status.id"), nullable=True, sort_order=6
    )
    education_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("education.id"), nullable=True, sort_order=7
    )

    title: Mapped[Optional[Title]] = relationship()
    maritalstatus: Mapped[Optional[MaritalStatus]] = relationship()
    gender: Mapped[Optional[Gender]] = relationship()
    education: Mapped[Optional[Education]] = relationship()

    @property
    def formatted_cpf(self) -> str:
        """Get the formatted CPF of the user"""
        value = self.cpf or "0"
        return re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", value.zfill(11))

    @property
    def identity(self) -> str | None:
        """Get the identity/document of the user"""
        return self.cpf

    @property
    def first_name(self) -> str:
        """Get the email of the user"""
        return self.nick_name or self.name.split(" ")[0]

    @validates("cpf")
    def validate_cpf(self, key, field: str) -> str:
        """validate CPF"""
        self.__logger.debug(f"Validating CPF: {key}-{field}")
        if field:
            field = re.sub(r"\D", "", field).zfill(CPF_SIZE)
            return field
        raise ValueError("CPF could not be null")


@event.listens_for(Person, "before_update", propagate=True)
def person_before_update_listener(mapper, connection, target):
    """before update listener"""
    LOGGER.debug(f"Mapper: {type(mapper)}-{str(mapper)}")
    LOGGER.debug(f"Connection: {type(connection)}-{str(connection)}")
    LOGGER.debug(f"Target: {type(target)}-{str(target)}")
    if isinstance(target, Person):
        target.time_updated = datetime.today()
