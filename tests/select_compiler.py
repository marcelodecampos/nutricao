#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module)
#
"""test module"""

from importlib import simple
from pprint import pprint
import sys
import os
from sqlalchemy import create_engine, MetaData, select, URL, text
from sqlalchemy.orm import Session, sessionmaker

# just in case
sys.path.append(os.getcwd())
from entities import *

# Database connection for minhnutri (PostgreSQL)
DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Curiosity killed the cat",  # plain (unescaped) text
    host="db.local",
    database="minhanutri",
    query={
        "application_name": "reflex",
    },
).render_as_string(False)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

pprint(globals())

entity_class = globals()["Person"]

query = """
    SELECT id, name, age, email,
    FROM person p inner join user_contac_document ucd
    LIMIT 10"""
with SessionLocal() as session:
    result = session.execute(query)
    for row in result:
        pprint(row._asdict())  # Convert RowProxy to dict for better readability
