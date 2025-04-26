"""Add a master login

Revision ID: df079276fc33
Revises: 749248e21515
Create Date: 2025-04-23 01:20:07.474890

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import Login

# revision identifiers, used by Alembic.
revision: str = "df079276fc33"
down_revision: Union[str, None] = "749248e21515"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "0370631a531f"


def upgrade() -> None:
    """Upgrade schema."""
    session: Session = Session(bind=op.get_bind())
    entitites = (Login(user_id=1, password="137375"),)
    session.add_all(entitites)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE login CASCADE")
