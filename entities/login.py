#!  python3
# -*- coding: utf-8 -*-
"""login entity modules"""

from datetime import datetime
import bcrypt

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
    Boolean,
    DateTime,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from utils.logger import get_logger
from .base import Base, InsertDate, InsertUpdateDate
from .person import User


LOGGER = get_logger("state")


login_fk = ForeignKey(
    "login.user_id",
    ondelete="CASCADE",
)


class Login(InsertUpdateDate):
    """login"""

    __tablename__ = "login"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        primary_key=True,
    )
    password: Mapped[str] = mapped_column(String(64))
    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )
    locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="f",
    )
    password_expires: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now() + interval '1 year'"),  # pylint: disable=not-callable
    )

    user: Mapped[User] = relationship(lazy="immediate")

    def __str__(self):
        return f"Login(), {self.user}"

    @validates("password")
    def validate_password(self, key: str, field: str) -> str:
        """crypt this password"""
        # TODO : validate password strength
        if field.startswith("$2b$") and len(field) >= 60:
            # already encrypted... pass
            return field
        msg = f"encrypting password {field}"
        LOGGER.debug(msg)
        hashed_password = bcrypt.hashpw(field.encode(), bcrypt.gensalt())
        return hashed_password.decode()


class LoginAudit(InsertDate, Base):
    """class audit login"""

    __tablename__ = "login_audit"
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("login.user_id", ondelete="CASCADE"),
    )
    ip_address: Mapped[str] = mapped_column(String(48))
    login: Mapped["Login"] = relationship(lazy="immediate")

    __pk = PrimaryKeyConstraint("user_id", "time_created")
    __created_at_key = Index("ix_login_audit_time_created", "time_created")
    __table_args__ = (__created_at_key, __pk)


class LastUsedPasswords(InsertDate):
    """class Last Used"""

    __tablename__ = "last_used_password"
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("login.user_id", ondelete="CASCADE"),
    )
    password: Mapped[str] = mapped_column(String(64))
    login: Mapped["Login"] = relationship(lazy="immediate")
    __pk = PrimaryKeyConstraint("user_id", "password")
    __table_args__ = (__pk,)
