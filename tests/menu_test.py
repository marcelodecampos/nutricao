"""Load data into menu

Revision ID: b9eda23299a6
Revises: 55d2ecc169e5
Create Date: 2025-05-08 01:28:41.167628

"""

from pprint import pprint
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from treelib import Node, Tree
import reflex as rx


def get_session():
    """get session for test purposes"""

    url = "postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=alembic"
    engine = create_engine(url)
    session = Session(engine)
    return session


def get_menu(session) -> Tree:
    """get menu"""
    query = text("SELECT * FROM vw_menu")
    stmt = session.execute(query)
    cursor_description = stmt.cursor.description
    menus = stmt.fetchall()
    tree: Tree = Tree()
    tree.create_node("Root", "root")
    for menu in menus:
        row = {}
        for name, value in zip((d[0] for d in cursor_description), menu):
            row[name] = value
        pprint(row)
        tree.create_node(row["name"], row["id"], row["parent_id"] or "root", row)
    tree.show()
    return tree


def create_sub_menu_item(menu_data: dict):
    return rx.menu.item({menu_data["name"]})


def create_sub_menu(menu_data: dict, menu_list: list):
    return rx.menu.sub(
        rx.menu.sub_trigger(menu_data["name"]),
        rx.menu.sub_content(menu_list),
    )


def create_menu(menu_tree: Tree, nodes: list[Node] | None = None, level: int = 0) -> list:
    if not nodes:
        nodes = menu_tree.children("root")
    menu_child_list: list | None = None
    menu_list: list = []
    for node_obj in nodes:
        tabs = "...." * level
        pprint(f"{tabs}Creating Menu: {node_obj.data['name'].upper()}")
        if not node_obj.is_leaf():
            menu_child_list = create_menu(
                menu_tree, menu_tree.children(node_obj.identifier), level + 1
            )
        if node_obj.is_leaf():
            str_menu_type = create_sub_menu_item(node_obj.data)
            menu_child_list = None
        else:
            str_menu_type = create_sub_menu(node_obj.data, menu_child_list)
        menu_list.append(str_menu_type)
    return menu_list


if __name__ == "__main__":
    with get_session() as db:
        main_menus = get_menu(db)
    complete_list = create_menu(main_menus, main_menus.children("root"))
    menu_structure = rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("wrench", size=15, stroke_width=1),
            ),
        ),
        rx.menu.content(complete_list),
    )
    print("THIS IS A COMPLETE LISTA OF MENU")
    pprint(menu_structure, indent=4)
