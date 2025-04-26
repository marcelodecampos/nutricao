"""local part of exr"""

from typing import Optional

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import SimpleTable, Name


class FoodGroup(SimpleTable):
    """Food Group"""

    __tablename__ = "food_group"


class FoodComponent(SimpleTable):
    """Food Group"""

    __tablename__ = "food_component"


class Food(Name):
    """Food table"""

    __tablename__ = "food"
    centific_name: Mapped[Optional[str]] = mapped_column(String(256))
    brand: Mapped[Optional[str]] = mapped_column(String(128))
    tbca_id: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    food_group_id: Mapped[Integer] = mapped_column(ForeignKey("food_group.id"), index=True)
    food_group: Mapped[FoodGroup] = relationship()


class FoodComposition(Name):
    """Food Group"""

    __tablename__ = "food_composition"
    value: Mapped[Optional[str]] = mapped_column(Numeric(precision=10, scale=4))
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), index=True)
    food: Mapped[Food] = relationship()
    food_component_id: Mapped[int] = mapped_column(ForeignKey("food_component.id"), index=True)
    food_component: Mapped[FoodComponent] = relationship()
