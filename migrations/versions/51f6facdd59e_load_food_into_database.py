"""Load Food into database

Revision ID: 51f6facdd59e
Revises: 26fc160a46bf
Create Date: 2025-04-23 00:27:04.887338

"""

import json

from pathlib import Path
from typing import Sequence, Union

from sqlalchemy import select
from sqlalchemy.orm import Session
from alembic import op

from entities import Food, FoodGroup

# revision identifiers, used by Alembic.
revision: str = "51f6facdd59e"
down_revision: Union[str, None] = "26fc160a46bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "01b7ee9b5f55"


FOODS_FILE = "migrations/foods.json"


def upgrade() -> None:
    """Upgrade schema."""
    session = Session(bind=op.get_bind())
    file_path: Path = Path(FOODS_FILE)
    if not file_path.exists():
        raise FileNotFoundError(FOODS_FILE)

    with file_path.open("r", encoding="utf-8") as file:
        foods = json.load(file)

    for food in foods:
        food_data = foods.get(food, {})
        entity = Food()
        entity.name = food_data.get("name")
        entity.centific_name = food_data.get("centific_name")
        entity.tbca_id = food_data.get("id")
        entity.brand = food_data.get("brand")
        food_group_name: str = food_data.get("group").upper().strip()
        stmt = select(FoodGroup).where(FoodGroup.name == food_group_name)
        result = session.execute(stmt)
        entity.food_group = result.scalar_one()
        session.add(entity)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE food CASCADE")
