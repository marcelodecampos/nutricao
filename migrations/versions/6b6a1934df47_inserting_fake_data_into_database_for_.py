"""Inserting fake data into database for testing purpose

Revision ID: 6b6a1934df47
Revises: 1a4d17b4efa4
Create Date: 2025-05-03 17:27:22.529404

"""
from operator import add
import sqlalchemy as sa
from typing import Sequence, Union
from faker import Faker
from sqlalchemy.orm import Session
from alembic import op
from entities import Person, UserContactDocument, ContactDocument, Login

# revision identifiers, used by Alembic.
revision: str = '6b6a1934df47'
down_revision: Union[str, None] = '1a4d17b4efa4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def add_person(session, faker:Faker, male:bool, nonbinary:bool=False)->Person:
    person = Person(
        name=faker.name_nonbinary() if nonbinary else faker.name_male() if male else faker.name_female(),
        birthdate=faker.date(),
        education_id=faker.random_int(min=1, max=10),
        title_id=2 if male else 3,
        gender_id=3 if nonbinary else 1 if male else 2,
        marital_status_id=faker.random_int(min=1, max=5),
    )
    person.add (
        UserContactDocument(
            contdoc=session.get(ContactDocument, 1),
            name=faker.cpf(),
            is_main=True,
        )
    )
    person.add (
        UserContactDocument(
            contdoc=session.get(ContactDocument, 3),
            name=faker.passport_number(),
            is_main=True,
        )
    )
    person.add (
        UserContactDocument(
            contdoc=session.get(ContactDocument, 8),
            name=faker.cellphone_number(),
            is_main=True,
        )
    )
    person.add (
        UserContactDocument(
            contdoc=session.get(ContactDocument, 10),
            name=faker.email(),
            is_main=True,
        )
    )
    return person

def upgrade() -> None:
    """Upgrade schema."""
    faker_data = Faker('pt_BR')
    session:Session = Session(bind=op.get_bind())
    entities = list()
    for loop in range(200_000):
        male = add_person(session, faker_data, True)
        entities.append(male)
        famale = add_person(session, faker_data, False)
        entities.append(famale)
        if loop % 100 == 0:
            entities.append(add_person(session, faker_data, False, True))
            print (f"Contando: {loop:04}")
        if loop % 300 == 0:
            entities.append(Login(user=male, password="123456"))
            entities.append(Login(user=famale, password="123456"))
        if loop % 10000 == 0:
            print (f"Commiting all: {loop:04}")
            session.add_all(entities)
            session.commit()
            entities = list()
    print (f"entities has {len(entities)} items")
    session.add_all(entities)
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    pass



if __name__ == "__main__":
    faker_data = Faker('pt_BR')
    print (faker_data.name())
    print (faker_data.date())
    print (faker_data.cpf())
