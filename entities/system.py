"""local part of exr"""

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixin import InsertUpdateDateMixin, IsValidMixin


class Menu(IsValidMixin, InsertUpdateDateMixin, Base):
    """system menu data class"""

    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, sort_order=1
    )
    name: Mapped[str] = mapped_column(
        String(32), nullable=False, sort_order=2, unique=True
    )
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

    parent = relationship("Menu", remote_side=[id], foreign_keys=[parent_id])

    def __str__(self):
        url = self.url if self.url else ""
        return f"{self.id:03d} - {self.name:<32} {url:<32} "

    def __eq__(self, other: object):
        if not other:
            return False
        if isinstance(other, Menu):
            return self.id == other.id
        if isinstance(other, (int | Integer | BigInteger)):
            return self.id == other
        return False

    def __lt__(self, other: object):
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
