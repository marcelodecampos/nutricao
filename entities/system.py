"""local part of exr"""

import json
from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, String, BigInteger, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import IsValid, Base


class Menu(IsValid, Base):
    """system menu data class"""

    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, sort_order=1)
    name: Mapped[str] = mapped_column(String(32), nullable=False, sort_order=2, unique=True)
    url: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        sort_order=4,
        unique=True,
    )
    icon: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, sort_order=5)
    index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, sort_order=6)
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("menu.id"),
        sort_order=7,
        nullable=True,
    )
    time_created: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        sort_order=98,
    )
    time_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),  # pylint: disable=not-callable
        sort_order=99,
    )

    parent = relationship("Menu", remote_side=[id], foreign_keys=[parent_id])

    def __str__(self):
        return f"User(id={self.id})"

    def __eq__(self, other: any):
        if not other:
            return False
        if isinstance(other, Menu):
            return self.id == other.id
        if isinstance(other, (int | Integer | BigInteger)):
            return self.id == other
        return False

    def __lt__(self, other: any):
        if not other:
            return False
        if isinstance(other, Menu):
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
