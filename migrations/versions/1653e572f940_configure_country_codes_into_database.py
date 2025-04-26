"""Configure Country Codes into database

Revision ID: 1653e572f940
Revises: 0370631a531f
Create Date: 2025-04-23 01:09:43.226717

"""

import json
from pathlib import Path
from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import Country

# revision identifiers, used by Alembic.
revision: str = "1653e572f940"
down_revision: Union[str, None] = "0370631a531f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"

COUNTRY_CODES_FILES = "migrations/country.json"


def upgrade() -> None:
    """Upgrade schema."""

    test_file: Path = Path(COUNTRY_CODES_FILES)
    if not test_file.exists():
        msgerr = f"{COUNTRY_CODES_FILES} not found"
        raise FileNotFoundError(msgerr)
    session: Session = Session(bind=op.get_bind())
    with test_file.open("rt", encoding="utf-8") as country_file:
        countries = json.load(country_file)
        for country in countries:
            entity = Country()
            entity.name = country["name"]
            entity.alpha_2 = country["alpha-2"]
            entity.alpha_3 = country["alpha-3"]
            entity.country_code = country["country-code"]
            entity.iso_3166_2 = country["iso_3166-2"]
            entity.region = country["region"]
            entity.sub_region = country["sub-region"]
            entity.intermediate_region = country["intermediate-region"]
            entity.region_code = country["region-code"]
            entity.sub_region_code = country["sub-region-code"]
            entity.intermediate_region_code = country["intermediate-region-code"]
            session.add(entity)
        session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE country CASCADE")
