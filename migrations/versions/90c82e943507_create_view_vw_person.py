"""Create view vw_person

Revision ID: 90c82e943507
Revises: 97f7d1a28ed9
Create Date: 2025-05-03 20:03:49.176317

"""

import sqlalchemy as sa
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "90c82e943507"
down_revision: Union[str, None] = "01b7ee9b5f55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def creeate_view_login() -> None:
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


def create_view_pessoa() -> None:
    """Upgrade schema."""
    query = """
        CREATE OR REPLACE VIEW public.vw_person
        AS
        SELECT u.id,
            u.name,
            u.nick_name,
            u.birthdate,
            u.person_type,
            p.gender_id,
            p.title_id,
            p.marital_status_id,
            p.education_id,
            u.time_created, u.time_updated,
            ( SELECT unnamed_subquery.documents
                FROM ( SELECT ucd.user_id,
                            array_agg(ucd.name) AS documents
                        FROM user_contact_document ucd
                        WHERE ucd.user_id = u.id
                        GROUP BY ucd.user_id) unnamed_subquery) AS documents
        FROM person p INNER JOIN users u ON u.id = p.id;
    """
    op.execute(query)


def upgrade() -> None:
    """Upgrade schema."""
    create_view_pessoa()
    creeate_view_login()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("drop view if exists vw_person")
    op.execute("drop view if exists vw_login")
