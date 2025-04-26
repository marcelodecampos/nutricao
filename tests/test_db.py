#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module)
#
"""test module"""

import logging
import json
from pathlib import Path
from contextlib import suppress

import pytest
from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy_schemadisplay import create_schema_graph
from entities.person import UserContactDocument

from entities import (
    Base,
    Person,
    Country,
    State,
    City,
    Gender,
    Title,
    ContactDocument,
    Education,
    MaritalStatus,
    Login,
    Food,
    FoodGroup,
    FoodComponent,
)

LOGGER = logging.getLogger(__name__)

CIDADAO_FILE = "C:/TMP/cidadaos.sql"

COUNTRY_CODES_FILES = "resources/country.json"
BR_STATES_FILE = "resources/br_states.json"
BR_CITIES_FILE = "resources/municipios_ibge.csv"
FOODS_FILE = "resources/foods.json"

engine = create_engine("postgresql+psycopg://db.local/sistema", echo=True, echo_pool=True)
session = Session(engine)


@pytest.mark.dependency()
def test_recreate_database():
    """load contry codes"""
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine, checkfirst=True)

    # create the pydot graph object by autoloading all tables via a bound metadata object
    db_url = "postgresql+psycopg://postgres:curious@db.local/sistema"
    graph = create_schema_graph(
        engine=create_engine(db_url),
        metadata=MetaData(db_url),
        show_datatypes=False,  # The image would get nasty big if we'd show the datatypes
        show_indexes=False,  # ditto for indexes
        rankdir="LR",  # From left to right (instead of top to bottom)
        concentrate=False,  # Don't try to join the relation lines together
    )
    graph.write_png("dbschema.png")  # write out the file


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_food_group():
    """teste food_group"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_food_component():
    """teste food_component"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_food_group"])
def test_foods():
    """teste foods"""
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


@pytest.mark.dependency(depends=["test_food_group"])
def test_contact_document():
    """Table Document Tests"""
    try:
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
        session.add_all(entitites)
        session.commit()
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_gender():
    """Gender Tests"""
    try:
        entitites = (
            Gender(name="Masculino"),
            Gender(name="Feminino"),
        )
        session.add_all(entitites)
        session.commit()
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_education():
    """Gender Tests"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_marital_status():
    """Gender Tests"""
    try:
        entitites = (
            MaritalStatus(name="Solteiro"),
            MaritalStatus(name="Casado"),
            MaritalStatus(name="Separado"),
            MaritalStatus(name="Divorciado"),
            MaritalStatus(name="Viuvo"),
        )
        session.add_all(entitites)
        session.commit()
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_gender"])
def test_title():
    """Gender Tests"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(
    depends=[
        "test_title",
        "test_education",
        "test_marital_status",
        "test_gender",
        "test_contact_document",
    ]
)
def test_person():
    """Person Tests"""
    cpf = "430.606.728 90"
    cpf = "529.161.976-72"
    cpf = "19.583.651-06"
    cpf = "729.663.519-34"
    cpf = "490.250.662-91"
    try:
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
        leila.add(
            UserContactDocument(contdoc=contdoc_type_cpf, name="490.250.662-91", is_main=True)
        )
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
        p = session.get(Person, 6)
        if p:
            session.delete(p)
        session.commit()
        p = session.get(Person, 2)
        if p:
            p.name += " E ainda tinha Marra da silveira"
            session.commit()
        arquivo: Path = Path(CIDADAO_FILE)
        if arquivo.exists():
            with arquivo.open(encoding="UTF-8") as f_pointer:
                line = f_pointer.readline()
                while line:
                    cpf, dados = line.split("|")
                    dados = dados.replace('\\\\"', "'")
                    dados = json.loads(dados)
                    birthdate: str = dados.get("dataNascimento")
                    if birthdate == "19700230":
                        birthdate = "19700228"
                    sexo = dados.get("sexo")
                    if sexo not in ("1", "2"):
                        sexo = "1"
                    p = Person(
                        name=dados.get("nome"),
                        gender_id=int(sexo),
                        birthdate=f"{birthdate[:4]}-{birthdate[4:6]}-{birthdate[6:]}",
                    )
                    p.add(UserContactDocument(contdoc=contdoc_type_cpf, name=cpf, is_main=True))
                    doc_id = dados.get("ddd") + dados.get("telefone")
                    if doc_id and len(doc_id) > 7:
                        p.add(UserContactDocument(contdoc=contdoc_type_cell, name=doc_id))
                    session.add(p)
                    with suppress(UnicodeDecodeError):
                        line = f_pointer.readline()
        session.commit()
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_country():
    """load contry codes"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_recreate_database"])
def test_br_states():
    """load contry codes"""
    try:
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
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_br_states"])
def test_br_cities():
    """load contry codes"""
    try:
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
        assert count > 1
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_person"])
def test_query_001():
    """teste query"""

    stmt = select(UserContactDocument).where(UserContactDocument.name == "59469390415")
    result = session.execute(stmt)
    contdoc: UserContactDocument = result.scalar_one()
    assert contdoc and contdoc.user
    msg = f"contdoc[name={contdoc.name}, type={contdoc.contdoc}"
    LOGGER.warning(msg)


@pytest.mark.dependency(depends=["test_person"])
def test_login():
    """login test"""
    try:
        entitites = (Login(user_id=1, password="137375"),)
        session.add_all(entitites)
        session.commit()
    except Exception:
        session.rollback()
        raise


@pytest.mark.dependency(depends=["test_login"])
def test_query_002():
    """teste query 002"""
    stmt = (
        select(Login)
        .join(UserContactDocument, Login.user_id == UserContactDocument.user_id)
        .where(UserContactDocument.name == "59469390415")
    )
    result = session.execute(stmt)
    entity: UserContactDocument = result.scalar_one()
    if entity:
        stmt = select(Login).where(Login.user_id == entity.user_id)
        result = session.execute(stmt)
        entity: Login = result.scalar_one()
        assert entity.user.name == "MARCELO DE CAMPOS"


@pytest.mark.dependency(depends=["test_login"])
def test_query_003():
    """teste query 002"""
    stmt = select(UserContactDocument).where(UserContactDocument.name == "don't exist")
    try:
        result = session.execute(stmt)
        result.scalar_one()
        raise RuntimeError("Should have no records")
    except NoResultFound:
        # expected
        pass


@pytest.mark.dependency(depends=["test_login"])
def test_query_004():
    """teste query 002"""
    stmt = select(UserContactDocument).where(UserContactDocument.name == "49025066291")
    result = session.execute(stmt)
    entity: UserContactDocument = result.scalar_one()
    if entity:
        stmt = select(Login).where(Login.user_id == entity.user_id)
        result = session.execute(stmt)
        try:
            entity: Login = result.scalar_one()
            raise RuntimeError("Should have no records")
        except NoResultFound:
            pass
