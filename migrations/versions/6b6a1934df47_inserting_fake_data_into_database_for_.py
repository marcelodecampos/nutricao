# pylint: disable=not-callable, missing-class-docstring, missing-function-docstring, too-few-public-methods, no-member

"""Inserting fake data into database for testing purpose

Revision ID: 6b6a1934df47
Revises: 1a4d17b4efa4
Create Date: 2025-05-03 17:27:22.529404

"""

from typing import Sequence, Union
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from alembic import op
from entities import Person, UserContactDocument, ContactDocument, Login


# revision identifiers, used by Alembic.
revision: str = "6b6a1934df47"
down_revision: Union[str, None] = "01b7ee9b5f55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

emails_dict = {}
cpfs_dict = {}


def add_person(session, faker: Faker, male: bool, nonbinary: bool = False) -> Person:
    faker_email = faker.email(False)
    cpf = faker.cpf()
    name = (
        faker.name_nonbinary() if nonbinary else faker.name_male() if male else faker.name_female()
    )
    while faker_email in emails_dict:
        faker_email = faker.email(False)
    emails_dict[faker_email] = name
    while cpf in cpfs_dict:
        cpf = faker.cpf()
    cpfs_dict[cpf] = name
    person = Person(
        name=name,
        birthdate=faker.date(),
        education_id=faker.random_int(min=1, max=10),
        title_id=2 if male else 3,
        gender_id=3 if nonbinary else 1 if male else 2,
        marital_status_id=faker.random_int(min=1, max=5),
        cpf=cpf,
        email=faker_email,
    )
    person.add(
        UserContactDocument(
            contdoc=session.get(ContactDocument, 3),
            name=faker.passport_number(),
            is_main=True,
        )
    )
    person.add(
        UserContactDocument(
            contdoc=session.get(ContactDocument, 8),
            name=faker.cellphone_number(),
            is_main=True,
        )
    )
    return person


def upgrade() -> None:
    """Upgrade schema."""
    faker_data = Faker("pt_BR")
    session: Session = Session(bind=op.get_bind())
    entities = list()
    for loop in range(200_000):
        male = add_person(session, faker_data, True)
        entities.append(male)
        female = add_person(session, faker_data, False)
        entities.append(female)
        if loop % 100 == 0:
            entities.append(add_person(session, faker_data, False, True))
            print(f"Contando: {loop:04}")
        if loop % 300 == 0:
            entities.append(Login(user=male, password="123456"))
            entities.append(Login(user=female, password="123456"))
        if loop % 10000 == 0:
            print(f"Commiting all: {loop:04} - {datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}")
    print(f"entities has {len(entities)} items")
    session.add_all(entities)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    pass


if __name__ == "__main__":
    faker_data = Faker("pt_BR")
    print(faker_data.name())
    print(faker_data.date())
    print(faker_data.cpf())
