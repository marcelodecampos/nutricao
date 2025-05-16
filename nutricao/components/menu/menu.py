# python3
# -*- coding: utf-8 -*-
# pylint: disable=(too-few-public-methods, inherit-non-class, missing-function-docstring)
"""init module for login component."""

from types import FunctionType
from typing import List
from sqlalchemy import select
import reflex as rx
from entities import Menu


class test(rx.Model):
    pass


class TestState(rx.State):
    """Class test state"""

    menu_ids: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    _list_of_options: List[Menu] = None

    @rx.event
    def on_mount(self):
        """on mount event"""
        self._list_of_options = []
        with rx.session() as session:
            query = select(Menu).where(
                (Menu.parent_id == None),
            )
            rows = session.exec(query).all()
            for row in rows:
                self._list_of_options.append(row[0])
                self.menu_ids.append(row[0].id)
            session.commit()


def get_some_itens() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Full name"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Group"),
            ),
        ),
        rx.table.body(
            rx.table.row(
                rx.table.row_header_cell("Danilo Sousa"),
                rx.table.cell("danilo@example.com"),
                rx.table.cell("Developer"),
            ),
            rx.table.row(
                rx.table.row_header_cell("Zahra Ambessa"),
                rx.table.cell("zahra@example.com"),
                rx.table.cell("Admin"),
            ),
            rx.table.row(
                rx.table.row_header_cell("Jasper Eriks"),
                rx.table.cell("jasper@example.com"),
                rx.table.cell("Developer"),
            ),
        ),
        width="100%",
    )


def create_acordion_item(item: int) -> rx.Component:
    item_value: str = f"id: {item}"
    return rx.accordion.item(
        header=f"some item {item}",
        content=f"some item{item}",
        value=item_value,
    )


def menu_layout(callback: FunctionType | None = None) -> rx.Component:
    """Create a common layout for the app."""
    return rx.accordion.root(
        rx.foreach(TestState.menu_ids, create_acordion_item),
        collapsible=True,
        width="300px",
        variant="ghost",
        spacing="0",
        paddding="0",
    )
