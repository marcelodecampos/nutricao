#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument, logging-fstring-interpolation, unsubscriptable-object)
"""Module File"""

import logging
import re
from datetime import date
from typing import Optional, Self

from dateutil.relativedelta import relativedelta
from sqlalchemy import CHAR, Boolean, Date, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..base import Base, Name, SimpleTable
from .constants import (
    CONTDOC_CHECK_CONSTRAINT,
    DEFAULT_NAME_FIELD_SIZE,
    EMAIL_REGEX,
    TYPE_PERSON_CHECK_CONSTRAINT,
)

LOGGER = logging.getLogger(__name__)


class ContactDocument(SimpleTable):
    """Base class User"""

    __tablename__ = "contact_document"
    mask: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, sort_order=3
    )
    allow_login: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="f", sort_order=4
    )
    validation_regex: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, sort_order=5
    )
    sub_regex: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, sort_order=6
    )
    contdoc_type: Mapped[str] = mapped_column(
        CHAR, CONTDOC_CHECK_CONSTRAINT, sort_order=7
    )
    person_type: Mapped[Optional[str]] = mapped_column(
        CHAR, TYPE_PERSON_CHECK_CONSTRAINT, nullable=True, sort_order=8
    )

    def __str__(self):
        return (
            super().__str__()
            + f", 'mask': {self.mask}, 'allow_origim': {self.allow_login}"
            + f", 'validation_regex': {self.validation_regex} "
            + f", 'sub_regex': {self.sub_regex} "
            + f", 'contdoc_type': {self.contdoc_type} "
            + f", 'person_type': {self.person_type} "
        )


class UserContactDocument(Base):
    """Relationship table user <---> contact_document"""

    __tablename__ = "user_contact_document"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    contdoc_id: Mapped[int] = mapped_column(
        ForeignKey("contact_document.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(128), index=True, primary_key=True)
    is_main: Mapped[bool] = mapped_column(Boolean, server_default="f", default=False)

    user: Mapped["User"] = relationship(back_populates="contact_document")
    contdoc: Mapped[ContactDocument] = relationship(
        lazy="joined",
        innerjoin=True,
    )

    @validates("name")
    def validate_name(self, key: str, field: str):
        """validate contdoc field"""
        if (
            self.contdoc
            and isinstance(self.contdoc, ContactDocument)
            and self.contdoc.sub_regex
        ):
            field = re.sub(self.contdoc.sub_regex, "", field)
        return field

    def __str__(self):
        return (
            f"User({self.user}, DocumentType({self.contdoc}), "
            f"Document({self.name}), {super().__str__()}"
        )


class User(Name):
    """Base class User"""

    __logger = logging.getLogger(__name__)
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_name", "name"),)
    __mapper_args__ = {
        "polymorphic_identity": "users",
        "polymorphic_on": "person_type",
    }
    nick_name: Mapped[Optional[str]] = mapped_column(
        String(DEFAULT_NAME_FIELD_SIZE),
        nullable=True,
        index=True,
        sort_order=3,
    )
    birthdate: Mapped[date] = mapped_column(
        Date(),
        nullable=True,
        sort_order=4,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(DEFAULT_NAME_FIELD_SIZE),
        nullable=True,
        unique=True,
        sort_order=2,
    )
    person_type: Mapped[str] = mapped_column(
        CHAR,
        TYPE_PERSON_CHECK_CONSTRAINT,
        sort_order=5,
    )

    contact_document: Mapped[Optional[list[UserContactDocument]]] = relationship(
        back_populates="user",
    )

    def add(self, new_item: UserContactDocument) -> Self:
        """add a document or contact to a user"""
        if not self.contact_document:
            self.contact_document = []
        new_item.user = self
        new_item.user_id = self.id
        self.contact_document.append(new_item)
        return self

    def __str__(self):
        return f"User(type={self.person_type}, birthdate={self.birthdate}, {super().__str__()}"

    @property
    def formatted_birthdate(self) -> str:
        """Get the birthdate of the user in a formatted string"""
        return self.birthdate.strftime("%d/%m/%Y") if self.birthdate else ""

    @property
    def age(self) -> Optional[int]:
        """Calculate the age of the user based on the birthdate"""
        if self.birthdate:
            return relativedelta(date.today(), self.birthdate).years
        return None

    @validates("email")
    def validate_email(self, key, field: str) -> str:
        """validate email"""
        self.__logger.debug(f"Validating email: {key}-{field}")
        if not field:
            errmsg = "E-mail could not be null"
            self.__logger.error(errmsg)
            raise ValueError(errmsg)
        if not re.fullmatch(EMAIL_REGEX, field):
            errmsg = f"Invalid e-mail format: {field}"
            self.__logger.error(errmsg)
            raise ValueError(errmsg)
        return field.strip().lower()
