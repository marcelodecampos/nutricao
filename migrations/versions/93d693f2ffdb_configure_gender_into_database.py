"""Configure gender into database

Revision ID: 93d693f2ffdb
Revises: 179b3c6dc748
Create Date: 2025-04-23 00:44:44.939680

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op

from entities import Gender

# revision identifiers, used by Alembic.
revision: str = "93d693f2ffdb"
down_revision: Union[str, None] = "179b3c6dc748"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    entitites = (
        Gender(name="Masculino"),
        Gender(name="Feminino"),
        Gender(name="Não Declarado"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE gender CASCADE")
