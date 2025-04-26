"""Configure Title into database

Revision ID: f2ff5e0234e3
Revises: d95940dea59e
Create Date: 2025-04-23 00:53:38.928424

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import Title

# revision identifiers, used by Alembic.
revision: str = "f2ff5e0234e3"
down_revision: Union[str, None] = "d95940dea59e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "93d693f2ffdb"


def upgrade() -> None:
    """Upgrade schema."""
    g_01 = (
        Title(name="Você", shortening="v."),
        Title(name="Doutor", shortening="Dr.", gender_id=1),
        Title(name="Doutora", shortening="Dra.", gender_id=2),
        Title(name="Senhor", shortening="Sr.", gender_id=1),
        Title(name="Senhora", shortening="Sra.", gender_id=2),
        Title(name="Senhorita", shortening="Srta.", gender_id=2),
        Title(name="Vossa Alteza", shortening="V.A."),
        Title(name="Vossa Excelência", shortening="V.Ex.a"),
        Title(name="Vossa Eminência", shortening="V.Ema"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(g_01)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE title CASCADE")
