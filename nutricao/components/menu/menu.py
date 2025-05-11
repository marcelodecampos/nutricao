# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""init module for login component."""

from datetime import datetime
from types import FunctionType
import reflex as rx
from sqlalchemy import select, text
from treelib import Node, Tree
from entities import Menu


class MenuState(rx.ComponentState):
    """Component state class for menus"""

    selected: bool = False

    @classmethod
    def sub_menu_content(cls):
        rx.menu.sub(
            rx.menu.sub_trigger("Tabelas de Pessoa"),
            rx.menu.sub_content(
                rx.menu.item("Escolaridade"),
                rx.menu.item("Gênero"),
                rx.menu.item("Estado Civil"),
                rx.menu.item("Pronome de Tratamento"),
                rx.menu.item("Tipo de Documento"),
                rx.menu.item("Meio de Contato"),
            ),
        )

    @classmethod
    def create_menu_tree(cls, menu_tree, n_index: int = 0):
        """create all menus"""
        submenu_compoment_list: list = []
        try:
            if not menu_tree[n_index].has_child:
                while not menu_tree[n_index].has_child:
                    submenu_compoment_list.append(rx.menu.item("Pais"))
                return submenu_compoment_list
            submenu_compoment_list = cls.create_menu_tree(menu_tree, menu_tree[n_index + 1])
        except KeyError:
            pass
        return submenu_compoment_list

    @classmethod
    def load_menu(cls) -> Tree:
        """get all menus from database without parent"""
        menu_tree: Tree = Tree()
        menu_tree.create_node("Root", "root")
        with rx.session() as session:
            query = text("SELECT * FROM vw_menu")
            stmt = session.exec(query)
            records: list = stmt.all()
            for row in records:
                menu_tree.create_node(row[1], row[0], row[5] or "root", row)
            session.commit()
        return cls.create_menu(menu_tree, menu_tree.children("root"))

    @classmethod
    def create_sub_menu_item(cls, menu_data: list):
        """return reflex sub menu item"""
        icon = None
        if menu_data[3]:
            icon = rx.icon(menu_data[3], size=15, stroke_width=1)
        text_element = rx.text(menu_data[1])
        return rx.menu.item(icon, text_element)

    @classmethod
    def create_sub_menu(cls, menu_data: list, menu_list: list):
        """return reflex sub menu"""
        return rx.menu.sub(
            rx.menu.sub_trigger(menu_data[1]),
            rx.menu.sub_content(menu_list),
        )

    @classmethod
    def create_menu(cls, menu_tree: Tree, nodes: list[Node] | None = None, level: int = 0) -> list:
        if not nodes:
            nodes = menu_tree.children("root")
        menu_child_list: list | None = None
        menu_list: list = []
        for node_obj in nodes:
            if not node_obj.is_leaf():
                menu_child_list = cls.create_menu(
                    menu_tree, menu_tree.children(node_obj.identifier), level + 1
                )
            if node_obj.is_leaf():
                str_menu_type = cls.create_sub_menu_item(node_obj.data)
                menu_child_list = None
            else:
                str_menu_type = cls.create_sub_menu(node_obj.data, menu_child_list)
            menu_list.append(str_menu_type)
        return menu_list

    @classmethod
    def menu_component_root(cls, menu_tree) -> rx.Component:
        """main class method that return components to refles"""
        rx_menu_item: rx.DropdownMenuRoot = rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("menu"),
                ),
            ),
            rx.menu.content(menu_tree),
            modal=False,
        )
        return rx_menu_item

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        """main class method that return components to reflex"""
        root = cls.menu_component_root(props["menu_tree"])
        return rx.box(
            rx.text(f"{datetime.now()}Debugging is so hard here!!!"),
            rx.vstack(
                root,
                spacing="0",
                padding="0",
            ),
            width="100wv",
            height="100hv",
            padding="0",
            spacing="0",
            display=["none", "none", "block"],
            position="sticky",
        )


def menu_layout(callback: FunctionType | None = None) -> rx.Component:
    """Create a common layout for the app."""
    menu_tree: Tree = MenuState.load_menu()
    return MenuState.create(menu_tree=menu_tree)
