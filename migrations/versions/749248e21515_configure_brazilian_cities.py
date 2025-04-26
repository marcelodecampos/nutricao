"""Configure Brazilian Cities

Revision ID: 749248e21515
Revises: 14b548b2908d
Create Date: 2025-04-23 01:19:00.800181

"""

from pathlib import Path
from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import City

# revision identifiers, used by Alembic.
revision: str = "749248e21515"
down_revision: Union[str, None] = "14b548b2908d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "14b548b2908d"

BR_CITIES_FILE = "migrations/municipios_ibge.csv"


def upgrade() -> None:
    """Upgrade schema."""
    session: Session = Session(bind=op.get_bind())
    test_file: Path = Path(BR_CITIES_FILE)
    if not test_file.exists():
        msgerr = f"{BR_CITIES_FILE} not found"
        raise FileNotFoundError(msgerr)
    with test_file.open("rt", encoding="utf-8") as city_file:
        lines = city_file.readlines()
        count = 0
        for line in lines:
            records = line.split(";")
            count += 1
            if count == 1:
                continue
            if records[0] == "UF" or not records[12]:
                continue
            entity = City()
            entity.name = records[12]
            entity.state_id = records[0]
            entity.code = records[10]
            session.add(entity)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE city CASCADE")
