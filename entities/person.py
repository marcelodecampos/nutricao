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

from . import Base, Name, SimpleTable, ContDocID, PersonType


TYPE_PERSON_CHECK_CONSTRAINT = CheckConstraint("person_type IN ('F', 'J', NULL)")
CONTDOC_CHECK_CONSTRAINT = CheckConstraint("contdoc_type IN ('C', 'D')")
CPF_SIZE = 11
CNPJ_SIZE = 14
STOP_CHARS = "[.-/_]"
DEFAULT_NAME_FIELD_SIZE = 256


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

    uk = UniqueConstraint("name", "gender_id")
    __table_args__ = (uk,)


class ContactDocument(SimpleTable):
    """Base class User"""

    __tablename__ = "contact_document"
    mask: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, sort_order=3)
    allow_login: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="f", sort_order=4
    )
    validation_regex: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, sort_order=5
    )
    sub_regex: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, sort_order=6)
    contdoc_type: Mapped[str] = mapped_column(CHAR, CONTDOC_CHECK_CONSTRAINT, sort_order=7)
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
    contdoc_id: Mapped[int] = mapped_column(ForeignKey("contact_document.id"), primary_key=True)
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
        if self.contdoc and isinstance(self.contdoc, ContactDocument) and self.contdoc.sub_regex:
            field = regex_substitute(self.contdoc.sub_regex, "", field)
        return field

    def __str__(self):
        return (
            f"User({self.user}, DocumentType({self.contdoc}), "
            f"Document({self.name}), {super().__str__()}"
        )


class User(Name):
    """Base class User"""

    __tablename__ = "users"
    __table_args__ = {
        "comment": (
            "This table uses plural in order to do not "
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
        sort_order=3,
    )
    birthdate: Mapped[date] = mapped_column(
        Date(),
        nullable=True,
        sort_order=4,
    )
    person_type: Mapped[str] = mapped_column(
        CHAR,
        TYPE_PERSON_CHECK_CONSTRAINT,
        sort_order=5,
    )

    contact_document: Mapped[Optional[list[UserContactDocument]]] = relationship(
        back_populates="user",
        lazy="joined",
        innerjoin=False,
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
    def email(self) -> str:
        """Get the email of the user"""
        for item in self.contact_document:
            if item.contdoc and item.contdoc_id == ContDocID.EMAIL.value:
                return item.name
        return ""


class Person(User):
    """Base class Person"""

    __tablename__ = "person"
    __mapper_args__ = {
        "polymorphic_identity": PersonType.PERSON.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), sort_order=1, primary_key=True
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
    def cpf(self) -> str:
        """Get the email of the user"""
        for item in self.contact_document:
            if item.contdoc and item.contdoc.id == ContDocID.CPF.value:
                return item.name
        return ""

    @property
    def first_name(self) -> str:
        """Get the email of the user"""
        return self.name.split(" ")[0]


class Company(User):
    """Base class Company"""

    __tablename__ = "company"
    __mapper_args__ = {
        "polymorphic_identity": PersonType.COMPANY.value,
    }

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, sort_order=3)

    @validates("cnpj")
    def validate_cnpj(self, key, field: str) -> str:
        """validate CPF"""
        if field:
            field = regex_substitute(STOP_CHARS, "", field)
            field = field.zfill(CNPJ_SIZE)
            return field
        raise ValueError("CPF could not be null")

    @property
    def cnpj(self) -> str:
        """Get the email of the user"""
        for item in self.contact_document:
            if item.contdoc and item.contdoc.id == 7:
                return item.name
        return ""
