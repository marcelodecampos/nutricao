"""local part of exr"""

from typing import Optional
import reflex as rx
from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import Field, Relationship
from .base import SimpleTable, Name, SimpleTableModel, NameModel


class FoodGroupModel(SimpleTableModel, rx.Model):
    """Food Group"""

    __tablename__ = "food_group"


class FoodGroup(SimpleTable):
    """Food Group"""

    __tablename__ = "food_group"


class FoodComponentModel(SimpleTableModel, rx.Model):
    """Food Group"""

    __tablename__ = "food_component"


class FoodComponent(SimpleTable):
    """Food Group"""

    __tablename__ = "food_component"


class FoodModel(NameModel, rx.Model):
    """Food table"""

    __tablename__ = "food"
    centific_name: Optional[str]
    brand: Optional[str]
    tbca_id: Optional[str]
    food_group_id: int = Field(foreign_key="food_group.id")
    food_group: FoodGroupModel = Relationship()


class Food(Name):
    """Food table"""

    __tablename__ = "food"
    centific_name: Mapped[Optional[str]] = mapped_column(String(256), sort_order=10)
    brand: Mapped[Optional[str]] = mapped_column(String(128), sort_order=11)
    tbca_id: Mapped[Optional[str]] = mapped_column(String(128), index=True, sort_order=12)
    food_group_id: Mapped[Integer] = mapped_column(
        ForeignKey("food_group.id"), index=True, sort_order=13
    )
    food_group: Mapped[FoodGroup] = relationship()


class FoodCompositionModel(NameModel, rx.Model):
    """Food Group"""

    value: Optional[str]
    food_id: int = Field(foreign_key="food.id")
    food: FoodModel = Relationship()
    food_component_id: int = Field(foreign_key="food_component.id")
    food_component: FoodComponentModel = Relationship()


class FoodComposition(Name):
    """Food Group"""

    __tablename__ = "food_composition"
    value: Mapped[Optional[str]] = mapped_column(Numeric(precision=10, scale=4), sort_order=10)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), index=True, sort_order=11)
    food: Mapped[Food] = relationship()
    food_component_id: Mapped[int] = mapped_column(
        ForeignKey("food_component.id"), index=True, sort_order=12
    )
    food_component: Mapped[FoodComponent] = relationship()
