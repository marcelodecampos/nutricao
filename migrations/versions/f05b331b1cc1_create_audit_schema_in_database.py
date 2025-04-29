"""Create audit schema in database

Revision ID: f05b331b1cc1
Revises: df079276fc33
Create Date: 2025-04-28 21:21:48.789511

"""

import sqlalchemy as sa
from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f05b331b1cc1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE SCHEMA IF NOT EXISTS audit;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP SCHEMA IF EXISTS audit;
        """
    )
