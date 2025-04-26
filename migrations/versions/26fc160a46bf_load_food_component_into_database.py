"""Load Food Component into Database

Revision ID: 26fc160a46bf
Revises: 01b7ee9b5f55
Create Date: 2025-04-23 00:19:14.179595

"""

from typing import Sequence, Union

from reflex import session
from sqlalchemy.orm import Session
from alembic import op
from entities import FoodComponent

# revision identifiers, used by Alembic.
revision: str = "26fc160a46bf"
down_revision: Union[str, None] = "01b7ee9b5f55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    g_01 = (
        FoodComponent(name="Ácidos graxos trans"),
        FoodComponent(name="Vitamina A (RAE)"),
        FoodComponent(name="Fósforo"),
        FoodComponent(name="Vitamina D"),
        FoodComponent(name="Cobre"),
        FoodComponent(name="Fibra alimentar"),
        FoodComponent(name="Tiamina"),
        FoodComponent(name="Ferro"),
        FoodComponent(name="Zinco"),
        FoodComponent(name="Carboidrato total"),
        FoodComponent(name="Açúcar de adição"),
        FoodComponent(name="Alfa-tocoferol (Vitamina E)"),
        FoodComponent(name="Cálcio"),
        FoodComponent(name="Sódio"),
        FoodComponent(name="Potássio"),
        FoodComponent(name="Vitamina B12"),
        FoodComponent(name="Cinzas"),
        FoodComponent(name="Selênio"),
        FoodComponent(name="Ácidos graxos monoinsaturados"),
        FoodComponent(name="Umidade"),
        FoodComponent(name="Sal de adição"),
        FoodComponent(name="Álcool"),
        FoodComponent(name="Vitamina C"),
        FoodComponent(name="Colesterol"),
        FoodComponent(name="Ácidos graxos poliinsaturados"),
        FoodComponent(name="Magnésio"),
        FoodComponent(name="Lipídios"),
        FoodComponent(name="Equivalente de folato"),
        FoodComponent(name="Riboflavina"),
        FoodComponent(name="Vitamina A (RE)"),
        FoodComponent(name="Carboidrato disponível"),
        FoodComponent(name="Manganês"),
        FoodComponent(name="Niacina"),
        FoodComponent(name="Energia"),
        FoodComponent(name="Vitamina B6"),
        FoodComponent(name="Ácidos graxos saturados"),
        FoodComponent(name="Proteína"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(g_01)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE food_component CASCADE")
