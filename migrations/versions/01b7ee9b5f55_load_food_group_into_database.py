"""Load Food Group into Database

Revision ID: 01b7ee9b5f55
Revises: 37117391b8b6
Create Date: 2025-04-22 23:58:47.599912

"""

from typing import Sequence, Union
from sqlalchemy.orm import Session

from alembic import op
from entities import FoodGroup


# revision identifiers, used by Alembic.
revision: str = "01b7ee9b5f55"
down_revision: Union[str, None] = "37117391b8b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    session = Session(bind=op.get_bind())
    g_01 = (
        FoodGroup(name="Pescados e frutos do mar"),
        FoodGroup(name="Alimentos industrializados"),
        FoodGroup(name="Ovos e derivados"),
        FoodGroup(name="Bebidas"),
        FoodGroup(name="Frutas e derivados"),
        FoodGroup(name="Açúcares e doces"),
        FoodGroup(name="Gorduras e óleos"),
        FoodGroup(name="Fast food"),
        FoodGroup(name="Leguminosas e derivados"),
        FoodGroup(name="Miscelâneas"),
        FoodGroup(name="Carnes e derivados"),
        FoodGroup(name="Nozes e sementes"),
        FoodGroup(name="Cereais e derivados"),
        FoodGroup(name="Leite e derivados"),
        FoodGroup(name="Vegetais e derivados"),
        FoodGroup(name="Alimentos para fins especiais"),
    )
    session.add_all(g_01)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE food_group CASCADE")
