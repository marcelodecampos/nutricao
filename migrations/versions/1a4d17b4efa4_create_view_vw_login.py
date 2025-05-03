"""Create View vw_login

Revision ID: 1a4d17b4efa4
Revises: 87826ec858af
Create Date: 2025-05-03 17:20:02.766170

"""
import sqlalchemy as sa
from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '1a4d17b4efa4'
down_revision: Union[str, None] = '87826ec858af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    query = """
        create or replace view vw_login as
        select
            u.id, name, nick_name, birthdate, person_type,  --users
            gender_id, title_id, marital_status_id, education_id, --person
            password, attempts, locked, password_expires, --login
            (select documents from (
                select ucd.user_id, array_agg(name) as documents from user_contact_document ucd
                where ucd.user_id = u.id
                group by user_id)
            ) as documents
        from
            login l
            inner join person p on l.user_id = p.id
            inner join users u on u.id = p.id
    """
    op.execute(query)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("drop view if exists vw_login")
    pass
