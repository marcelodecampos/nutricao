"""Configura Brazilian States

Revision ID: 14b548b2908d
Revises: 1653e572f940
Create Date: 2025-04-23 01:18:18.344181

"""

import json
from pathlib import Path
from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import State

# revision identifiers, used by Alembic.
revision: str = "14b548b2908d"
down_revision: Union[str, None] = "1653e572f940"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"

BR_STATES_FILE = "migrations/br_states.json"


def upgrade() -> None:
    """Upgrade schema."""
    session: Session = Session(bind=op.get_bind())
    test_file: Path = Path(BR_STATES_FILE)
    if not test_file.exists():
        msgerr = f"{BR_STATES_FILE} not found"
        raise FileNotFoundError(msgerr)
    with test_file.open("rt", encoding="utf-8") as state_file:
        states = json.load(state_file)
        for state in states:
            entity = State()
            entity.name = state["nome"]
            entity.shortening = state["uf"]
            entity.code = state["codigo_uf"]
            entity.latitude = state["latitude"]
            entity.longitude = state["longitude"]
            session.add(entity)
        session.commit()
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE state CASCADE")
