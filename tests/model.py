#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module)
#
"""test module"""

from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph


url = (
    "postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=menu_test"
)
engine = create_engine(url)
metadata = MetaData()
metadata.reflect(bind=engine)

graph = create_schema_graph(
    engine,
    metadata=metadata,
    show_datatypes=True,  # The image would get nasty big if we'd show the datatypes
    show_indexes=True,  # ditto for indexes
    rankdir="LR",  # From left to right (instead of top to bottom)
    concentrate=False,  # Don't try to join the relation lines together
)
graph.write_png("dbschema.png")  # write out the file
