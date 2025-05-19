"""Load Food Group into Database

Revision ID: 01b7ee9b5f55
Revises: 37117391b8b6
Create Date: 2025-04-22 23:58:47.599912

"""

import json
from pathlib import Path
from typing import Sequence, Union
from sqlalchemy import select
from sqlalchemy.orm import Session

from alembic import op
from entities import (
    FoodGroup,
    FoodComponent,
    Food,
    City,
    Title,
    MaritalStatus,
    Country,
    ContactDocument,
    Gender,
    State,
    Education,
    Person,
    UserContactDocument,
    Login,
)


# revision identifiers, used by Alembic.
revision: str = "01b7ee9b5f55"
down_revision: Union[str, None] = "37117391b8b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


FOODS_FILE = "migrations/foods.json"
BR_CITIES_FILE = "migrations/municipios_ibge.csv"
COUNTRY_CODES_FILES = "migrations/country.json"
BR_STATES_FILE = "migrations/br_states.json"


def load_education(session) -> None:
    """Upgrade schema."""
    entitites = (
        Education(name="Analfabeto"),
        Education(name="Fundamental Incompleto"),
        Education(name="Fundamental Completo"),
        Education(name="Médio Incompleto"),
        Education(name="Médio Completo"),
        Education(name="Superior Completo"),
        Education(name="Pós-Graduação completo"),
        Education(name="Mestrado completo"),
        Education(name="Doutorado completo"),
        Education(name="Pós-Doutorado completo"),
    )
    session.add_all(entitites)
    session.commit()


def load_gender(session) -> None:
    """Upgrade schema."""
    entitites = (
        Gender(name="Masculino"),
        Gender(name="Feminino"),
        Gender(name="Não Declarado"),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()


def load_contact_document(session) -> None:
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
            allow_login=False,
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
            allow_login=True,
            contdoc_type="C",
        ),
    )
    session: Session = Session(bind=op.get_bind())
    session.add_all(entitites)
    session.commit()


def load_country(session) -> None:
    """Upgrade schema."""

    test_file: Path = Path(COUNTRY_CODES_FILES)
    if not test_file.exists():
        msgerr = f"{COUNTRY_CODES_FILES} not found"
        raise FileNotFoundError(msgerr)
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


def load_br_states(session) -> None:
    """Upgrade schema."""
    load_country(session)
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


def load_marital_status(session) -> None:
    """Upgrade schema."""
    entitites = (
        MaritalStatus(name="Solteiro"),
        MaritalStatus(name="Casado"),
        MaritalStatus(name="Separado"),
        MaritalStatus(name="Divorciado"),
        MaritalStatus(name="Viuvo"),
    )
    session.add_all(entitites)
    session.commit()


def load_title(session) -> None:
    """Upgrade schema."""
    load_gender(session)
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
    session.add_all(g_01)
    session.commit()


def load_city(session) -> None:
    """Upgrade schema."""
    load_br_states(session)
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


def load_food_group(session):
    g_01 = (
        FoodGroup(name="Pescados e frutos do mar"),
        FoodGroup(name="Alimentos industrializados"),
        FoodGroup(name="Ovos e derivados"),
        FoodGroup(name="Bebidas"),
        FoodGroup(name="Frutas e derivados"),
        FoodGroup(name="Açúcares e doces"),
        FoodGroup(name="Gorduras e óleos"),
        FoodGroup(name="Fast food"),
        FoodGroup(name="Leguminosas e derivados"),
        FoodGroup(name="Miscelâneas"),
        FoodGroup(name="Carnes e derivados"),
        FoodGroup(name="Nozes e sementes"),
        FoodGroup(name="Cereais e derivados"),
        FoodGroup(name="Leite e derivados"),
        FoodGroup(name="Vegetais e derivados"),
        FoodGroup(name="Alimentos para fins especiais"),
    )
    session.add_all(g_01)
    session.commit()


def load_food_component(session):
    g_01 = (
        FoodComponent(name="Ácidos graxos trans"),
        FoodComponent(name="Vitamina A (RAE)"),
        FoodComponent(name="Fósforo"),
        FoodComponent(name="Vitamina D"),
        FoodComponent(name="Cobre"),
        FoodComponent(name="Fibra alimentar"),
        FoodComponent(name="Tiamina"),
        FoodComponent(name="Ferro"),
        FoodComponent(name="Zinco"),
        FoodComponent(name="Carboidrato total"),
        FoodComponent(name="Açúcar de adição"),
        FoodComponent(name="Alfa-tocoferol (Vitamina E)"),
        FoodComponent(name="Cálcio"),
        FoodComponent(name="Sódio"),
        FoodComponent(name="Potássio"),
        FoodComponent(name="Vitamina B12"),
        FoodComponent(name="Cinzas"),
        FoodComponent(name="Selênio"),
        FoodComponent(name="Ácidos graxos monoinsaturados"),
        FoodComponent(name="Umidade"),
        FoodComponent(name="Sal de adição"),
        FoodComponent(name="Álcool"),
        FoodComponent(name="Vitamina C"),
        FoodComponent(name="Colesterol"),
        FoodComponent(name="Ácidos graxos poliinsaturados"),
        FoodComponent(name="Magnésio"),
        FoodComponent(name="Lipídios"),
        FoodComponent(name="Equivalente de folato"),
        FoodComponent(name="Riboflavina"),
        FoodComponent(name="Vitamina A (RE)"),
        FoodComponent(name="Carboidrato disponível"),
        FoodComponent(name="Manganês"),
        FoodComponent(name="Niacina"),
        FoodComponent(name="Energia"),
        FoodComponent(name="Vitamina B6"),
        FoodComponent(name="Ácidos graxos saturados"),
        FoodComponent(name="Proteína"),
    )
    session.add_all(g_01)
    session.commit()


def load_food(session) -> None:
    """Upgrade schema."""
    load_food_group(session)
    file_path: Path = Path(FOODS_FILE)
    if not file_path.exists():
        raise FileNotFoundError(FOODS_FILE)

    with file_path.open("r", encoding="utf-8") as file:
        foods = json.load(file)

    for food in foods:
        food_data = foods.get(food, {})
        entity = Food()
        entity.name = food_data.get("name")
        entity.centific_name = food_data.get("centific_name")
        entity.tbca_id = food_data.get("id")
        entity.brand = food_data.get("brand")
        food_group_name: str = food_data.get("group").upper().strip()
        stmt = select(FoodGroup).where(FoodGroup.name == food_group_name)
        result = session.execute(stmt)
        entity.food_group = result.scalar_one()
        session.add(entity)
    session.commit()


def load_person(session) -> None:
    """Upgrade schema."""
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


def add_master_login(session) -> None:
    """Upgrade schema."""
    entitites = (Login(user_id=1, password="137375"),)
    session.add_all(entitites)
    session.commit()


def upgrade() -> None:
    """Upgrade schema."""
    session = Session(bind=op.get_bind())

    load_food_component(session)
    load_food(session)
    load_education(session)
    load_marital_status(session)
    load_title(session)
    load_contact_document(session)
    load_city(session)
    load_person(session)
    add_master_login(session)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE login CASCADE")
    op.execute("TRUNCATE TABLE food CASCADE")
    op.execute("TRUNCATE TABLE food_group CASCADE")
    op.execute("TRUNCATE TABLE food_component CASCADE")
    op.execute("TRUNCATE TABLE city CASCADE")
    op.execute("TRUNCATE TABLE title CASCADE")
    op.execute("TRUNCATE TABLE marital_status CASCADE")
    op.execute("TRUNCATE TABLE city CASCADE")
    op.execute("TRUNCATE TABLE country CASCADE")
    op.execute("TRUNCATE TABLE contact_document CASCADE")
    op.execute("TRUNCATE TABLE gender CASCADE")
    op.execute("TRUNCATE TABLE state CASCADE")
    op.execute("TRUNCATE TABLE education CASCADE")
    op.execute("TRUNCATE TABLE title CASCADE")
