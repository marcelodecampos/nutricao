# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""init module for login component."""

from datetime import datetime
from types import FunctionType
import reflex as rx
from sqlalchemy import select
from entities import Menu


menu_tree = []


def get_menu(session, parent=None, tabs=0):
    """get menu"""
    query = select(Menu).where(Menu.parent == parent).order_by(Menu.index)
    stmt = session.execute(query)
    for menu in stmt.scalars():
        menu_tree.append(menu)
        get_menu(session, menu, tabs + 1)


def load_menu() -> list:
    """on load event"""
    with rx.session() as session:
        if not menu_tree:
            get_menu(session)
    return menu_tree


def group(menu: Menu):
    """group"""
    return rx.el.li(
        rx.link(
            rx.el.h5(
                menu.name,
                class_name="font-smbold text-[0.875rem] text-slate-12 hover:text-violet-9 leading-5 tracking-[-0.01313rem] transition-color",
            ),
            underline="none",
            class_name="py-3",
        ),
        class_name="flex flex-col items-start ml-0 w-full",
    )


class MenuState(rx.ComponentState):
    """Component state class for menus"""

    selected: bool = False

    @classmethod
    def normalize_menu_structure(cls, entities: list[list]):
        from pprint import pprint

        normalized_menu = {}

        pprint(f"{datetime.now()}")
        pprint(entities)
        pass

    @classmethod
    def load_menu(cls) -> list:
        """get all menus from database without parent"""
        entities: list[list] = []
        with rx.session() as session:
            query = select(Menu).order_by(Menu.index)
            records: list[Menu] = session.execute(query).scalars()
            for item in records:
                entities.append((item.id, item.name, item.icon, item.url, item.parent_id))
        cls.normalize_menu_structure(entities)
        return entities

    @classmethod
    def menu_component(cls, text: str) -> rx.Component:
        """main class method that return components to refles"""
        return rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("wrench", size=15, stroke_width=1),
                    text,
                ),
            ),
            rx.menu.content(
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
                ),
                rx.menu.sub(
                    rx.menu.sub_trigger("Tabelas de Localidade"),
                    rx.menu.sub_content(
                        rx.menu.item("Pais"),
                        rx.menu.item("Estado"),
                        rx.menu.item("Cidade"),
                    ),
                ),
                rx.menu.sub(
                    rx.menu.sub_trigger("Tabelas de Nutrição"),
                    rx.menu.sub_content(
                        rx.menu.item("Alimentos"),
                        rx.menu.item("Grupo de Alimentos"),
                        rx.menu.item("Composição Alimentar"),
                    ),
                ),
            ),
            modal=False,
        )

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        """main class method that return components to reflex"""
        menus: list[list] = cls.load_menu()
        return rx.box(
            rx.text(f"{datetime.now()}Debugging is so hard here!!!"),
            rx.vstack(
                [cls.menu_component(item[1]) for item in menus],
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


def menu_sidebar_item(
    header: str,
    value: str,
    content: str | rx.Component | None = None,
    url: str | None = None,
) -> rx.Component:
    if not url:
        url = "#"
    return rx.box(
        rx.link(
            rx.hstack(
                rx.text(
                    header,
                    padding="0",
                    spacing="0",
                ),
                rx.icon(
                    "arrow-right",
                    padding="0",
                    spacing="0",
                    stroke_width=1,
                    size=20,
                ),
                align="center",
                width="100%",
                padding="0",
                spacing="0",
            ),
            href=url,
            width="100%",
            padding="0",
            spacing="0",
        ),
    )


def menu_layout(callback: FunctionType | None = None) -> rx.Component:
    """Create a common layout for the app."""
    return MenuState.create()
