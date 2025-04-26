"""local part of exr"""

from typing import Optional

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import SimpleTable, Name, SerialID, InsertUpdateDate


class Country(SimpleTable):
    """Iso country codes and Internationaç name"""

    __tablename__ = "country"
    alpha_2: Mapped[str] = mapped_column(String(2))
    alpha_3: Mapped[str] = mapped_column(String(3))
    country_code: Mapped[str] = mapped_column(String(3))
    iso_3166_2: Mapped[str] = mapped_column(String(16))
    region: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    sub_region: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    intermediate_region: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    region_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    sub_region_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    intermediate_region_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)


class State(SimpleTable):
    """Brazil: unidade de federacao"""

    __tablename__ = "state"
    shortening: Mapped[str] = mapped_column(String(2), unique=True)
    code: Mapped[int] = mapped_column(Integer, unique=True)
    latitude: Mapped[float] = mapped_column(Numeric(8, 3))
    longitude: Mapped[float] = mapped_column(Numeric(8, 3))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), default="32")

    country: Mapped[Country] = relationship()


class City(Name):
    """Brazil: municipio"""

    __tablename__ = "city"

    code: Mapped[str] = mapped_column(String(5))
    state_id: Mapped[int] = mapped_column(ForeignKey("state.code"))
    state: Mapped[State] = relationship()

    uk = UniqueConstraint("state_id", "code", name="uk_city_code_state_id")
    name_key = Index("ix_city_name", "name")
    __table_args__ = (uk, name_key)


class Address(SerialID, InsertUpdateDate):
    """address table"""

    __tablename__ = "address"
    address: Mapped[str] = mapped_column(String(128))
    complement: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    zip_code: Mapped[str] = mapped_column(String(10))
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped[City] = relationship()
