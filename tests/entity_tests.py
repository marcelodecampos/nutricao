"""Load data into menu

Revision ID: b9eda23299a6
Revises: 55d2ecc169e5
Create Date: 2025-05-08 01:28:41.167628

"""

from pprint import pprint
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from treelib import Node, Tree
import reflex as rx

try:
    from entities import Menu
except ImportError:
    import sys
    import os

    # just in case
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    sys.path.append(parent_directory)
    sys.path.append(current_directory)
    from entities import Menu


def get_session() -> Session:
    """get session for test purposes"""

    url = "postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=menu_test"
    engine = create_engine(url, echo=True, echo_pool=True)
    session = Session(engine)
    return session


def get_menu(session) -> list:
    """get menu"""
    try:
        stmt = session.execute(select(Menu))
        results: list = stmt.all()
        session.commit()
        return results
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":
    with get_session() as db:
        main_menus = get_menu(db)
        db.commit()
    print(type(main_menus))
    print(type(main_menus[0]))
