"""Configure education into database

Revision ID: 6be78570d2eb
Revises: 93d693f2ffdb
Create Date: 2025-04-23 00:51:43.736883

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import Education

# revision identifiers, used by Alembic.
revision: str = "6be78570d2eb"
down_revision: Union[str, None] = "93d693f2ffdb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    entitites = (
        Education(name="Analfabeto"),
        Education(name="Fundamental Incompleto"),
        Education(name="Fundamental Completo"),
        Education(name="Médio Incompleto"),
        Education(name="Médio Completo"),
        Education(name="Superior Completo"),
        Education(name="Pós-Graduação completo"),
        Education(name="Mestrado completo"),
        Education(name="Doutorado completo"),
        Education(name="Pós-Doutorado completo"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE education CASCADE")
    pass
