"""Configure Person into database

Revision ID: 0370631a531f
Revises: f2ff5e0234e3
Create Date: 2025-04-23 00:57:38.977461

"""

from typing import Sequence, Union

from sqlalchemy.orm import Session
from alembic import op
from entities import ContactDocument, Person, UserContactDocument

# revision identifiers, used by Alembic.
revision: str = "0370631a531f"
down_revision: Union[str, None] = "f2ff5e0234e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = [
    "f2ff5e0234e3",
    "d95940dea59e",
    "6be78570d2eb",
    "179b3c6dc748",
]


def upgrade() -> None:
    """Upgrade schema."""
    session: Session = Session(bind=op.get_bind())
    contdoc_type_cpf = session.get(ContactDocument, 1)
    contdoc_type_gc = session.get(ContactDocument, 3)
    contdoc_type_cell = session.get(ContactDocument, 8)
    contdoc_type_email = session.get(ContactDocument, 10)
    marcelo = Person(
        name="marcelo de campos",
        birthdate="1973-10-14",
        education_id=7,
        title_id=4,
        gender_id=1,
        marital_status_id=4,
    )
    marcelo.add(
        UserContactDocument(
            contdoc=contdoc_type_cpf,
            name="594.693.904-15",
            is_main=True,
        )
    )
    marcelo.add(
        UserContactDocument(
            contdoc=contdoc_type_gc,
            name="1023322 SSP DF",
            is_main=True,
        )
    )
    marcelo.add(
        UserContactDocument(
            contdoc=contdoc_type_cell,
            name="(61) 984017586)",
            is_main=True,
        )
    )
    marcelo.add(
        UserContactDocument(
            contdoc=contdoc_type_email,
            name="marcelo@cnj.jus.br",
            is_main=True,
        )
    )
    marcelo.add(
        UserContactDocument(
            contdoc=contdoc_type_email,
            name="sr.marcelo.campos@gmail.com",
            is_main=True,
        )
    )
    leila = Person(
        name="Cármen Leila da Costa Terra das Neves",
        birthdate="1977-07-27",
        education_id=6,
        title_id=5,
        gender_id=2,
        marital_status_id=3,
    )
    leila.add(UserContactDocument(contdoc=contdoc_type_cpf, name="490.250.662-91", is_main=True))
    p_01 = (
        marcelo,
        leila,
        Person(name="Helena Azevedo de Campos", birthdate="2009-11-20"),
        Person(name="Fernanda Terra das Neves Marra da Silveira", birthdate="2004-08-07"),
        Person(
            name="Júlia Terra das Neves Marra da Silveira",
            birthdate="2000-03-22",
        ),
        Person(
            name="bárbara Terra das Neves Marra da Silveira",
        ),
    )
    session.add_all(p_01)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE person CASCADE")
