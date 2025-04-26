"""Configure contact document into database

Revision ID: 179b3c6dc748
Revises: 51f6facdd59e
Create Date: 2025-04-23 00:38:33.741103

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import ContactDocument


# revision identifiers, used by Alembic.
revision: str = "179b3c6dc748"
down_revision: Union[str, None] = "51f6facdd59e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "37117391b8b6"


def upgrade() -> None:
    """Upgrade schema."""
    entitites = (
        ContactDocument(
            name="CPF",
            allow_login=True,
            mask="999.999.999-99",
            contdoc_type="D",
            sub_regex="[^0-9]",
        ),
        ContactDocument(name="Passaporte", contdoc_type="D", person_type="F"),
        ContactDocument(name="Identidade", contdoc_type="D", person_type="F"),
        ContactDocument(name="PIS/PASEP", contdoc_type="D", person_type="F"),
        ContactDocument(name="Tit. Eleitor", contdoc_type="D", person_type="F"),
        ContactDocument(name="Certidão de Nascimento", contdoc_type="D", person_type="F"),
        ContactDocument(
            name="CNPJ",
            allow_login=True,
            mask="99.999.999/9999-99",
            contdoc_type="D",
            person_type="J",
            sub_regex="[^0-9]",
        ),
        ContactDocument(
            name="Celular",
            allow_login=True,
            mask="(99) 99999-9999",
            contdoc_type="C",
            sub_regex="[^0-9]",
        ),
        ContactDocument(
            name="Telefone",
            mask="(99) 99999-9999",
            contdoc_type="C",
            sub_regex="[^0-9]",
        ),
        ContactDocument(
            name="e-mail",
            contdoc_type="C",
        ),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE contact_document CASCADE")
