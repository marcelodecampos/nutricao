#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, unused-argument)
"""Module File"""

from re import sub as regex_substitute
from typing import Optional, Self
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

from .base import Base, Name, SimpleTable, DEFAULT_NAME_FIELD_SIZE

TYPE_PERSON_CHECK_CONSTRAINT = CheckConstraint("person_type IN ('F', 'J', NULL)")
CONTDOC_CHECK_CONSTRAINT = CheckConstraint("contdoc_type IN ('C', 'D')")
CPF_SIZE = 11
CNPJ_SIZE = 14
STOP_CHARS = "[.-/_]"


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
    gender_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gender.id"), nullable=True)
    shortening: Mapped[str] = mapped_column(String(32))

    gender: Mapped[Optional[Gender]] = relationship(lazy="immediate")

    uk = UniqueConstraint("name", "gender_id")
    __table_args__ = (uk,)


class ContactDocument(SimpleTable):
    """Base class User"""

    __tablename__ = "contact_document"
    mask: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    allow_login: Mapped[bool] = mapped_column(Boolean, default=False, server_default="f")
    validation_regex: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    sub_regex: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    contdoc_type: Mapped[str] = mapped_column(
        CHAR,
        CONTDOC_CHECK_CONSTRAINT,
    )
    person_type: Mapped[Optional[str]] = mapped_column(
        CHAR, TYPE_PERSON_CHECK_CONSTRAINT, nullable=True
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    contdoc_id: Mapped[int] = mapped_column(ForeignKey("contact_document.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), index=True, primary_key=True)
    is_main: Mapped[bool] = mapped_column(Boolean, server_default="f", default=False)

    user: Mapped["User"] = relationship(back_populates="contact_document")
    contdoc: Mapped[ContactDocument] = relationship()

    @validates("name")
    def validate_name(self, key: str, field: str):
        """validate contdoc field"""
        if self.contdoc and isinstance(self.contdoc, ContactDocument) and self.contdoc.sub_regex:
            field = regex_substitute(self.contdoc.sub_regex, "", field)
        return field

    def __str__(self):
        return f"User({self.user}, DocumentType({self.contdoc}), Document({self.name}), {super().__str__()}"


class User(Name):
    """Base class User"""

    __tablename__ = "users"
    __table_args__ = {
        "comment": (
            "This table uses plural in order to do not"
            "conflict with user reserved word in some databases."
        )
    }
    __mapper_args__ = {
        "polymorphic_identity": "users",
        "polymorphic_on": "person_type",
    }
    nick_name: Mapped[Optional[str]] = mapped_column(
        String(DEFAULT_NAME_FIELD_SIZE),
        nullable=True,
        index=True,
    )
    birthdate: Mapped[date] = mapped_column(
        Date(),
        nullable=True,
    )
    person_type: Mapped[str] = mapped_column(
        CHAR,
        TYPE_PERSON_CHECK_CONSTRAINT,
    )

    contact_document: Mapped[Optional[list[UserContactDocument]]] = relationship(
        back_populates="user",
    )

    def add(self, new_item: UserContactDocument) -> Self:
        """add a document or contact to a user"""
        if not self.contact_document:
            self.contact_document = []
        new_item.user = self
        self.contact_document.append(new_item)
        return self

    def __str__(self):
        return f"User(type={self.person_type}, birthdate={self.birthdate}, {super().__str__()}"


class Person(User):
    """Base class Person"""

    __tablename__ = "person"
    __mapper_args__ = {
        "polymorphic_identity": "F",
    }

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    gender_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gender.id"), nullable=True)
    title_id: Mapped[Optional[int]] = mapped_column(ForeignKey("title.id"), nullable=True)
    marital_status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("marital_status.id"), nullable=True
    )
    education_id: Mapped[Optional[int]] = mapped_column(ForeignKey("education.id"), nullable=True)

    title: Mapped[Optional[Title]] = relationship()
    maritalstatus: Mapped[Optional[MaritalStatus]] = relationship()
    gender: Mapped[Optional[Gender]] = relationship()
    education: Mapped[Optional[Education]] = relationship()


class Company(User):
    """Base class Company"""

    __tablename__ = "company"
    __mapper_args__ = {
        "polymorphic_identity": "J",
    }

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    cnpj: Mapped[str] = mapped_column(
        String(CNPJ_SIZE + len(STOP_CHARS)), unique=True, nullable=False
    )

    @validates("cnpj")
    def validate_cpf(self, key, field: str) -> str:
        """validate CPF"""
        if field:
            field = regex_substitute(STOP_CHARS, "", field)
            field = field.zfill(CNPJ_SIZE)
            return field
        raise ValueError("CPF could not be null")
