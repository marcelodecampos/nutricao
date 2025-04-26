"""Configure MaritalStatus into database

Revision ID: d95940dea59e
Revises: 6be78570d2eb
Create Date: 2025-04-23 00:52:07.561010

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import MaritalStatus

# revision identifiers, used by Alembic.
revision: str = "d95940dea59e"
down_revision: Union[str, None] = "6be78570d2eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    entitites = (
        MaritalStatus(name="Solteiro"),
        MaritalStatus(name="Casado"),
        MaritalStatus(name="Separado"),
        MaritalStatus(name="Divorciado"),
        MaritalStatus(name="Viuvo"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()
    pass


def downgrade() -> None:
    op.execute("TRUNCATE TABLE marital_status CASCADE")
