#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import reflex as rx

from .multi_select_column import conditional_row_select_cell
from .simple_table_header import simple_table_header
from .simple_table_state import SimpleTableState
from .simple_table_title import simple_table_title


def simple_table_row_cell(cell_value, rowindex: int, colindex: int) -> rx.Component:
    """Create a simple table cell component."""
    return rx.table.cell(
        rx.text(cell_value, id=f"simple-table-cell-text-{rowindex}-{colindex}"),
        border="1px solid rgb(100, 100, 100)",
    )


def simple_table_row(index: int) -> rx.Component:
    """Create a simple table component."""
    return rx.table.row(
        conditional_row_select_cell(
            SimpleTableState.multiple_select,
            index,
            SimpleTableState.selected_items,
            SimpleTableState.handle_checkbox_on_change,
        ),
        rx.foreach(
            SimpleTableState.data[index],
            lambda record, colindex: simple_table_row_cell(record, index, colindex),
        ),
        id="simple-table-row",
        _hover={"background_color": "rgba(100, 100, 100, 0.2)"},
    )


def simple_table_body() -> rx.Component:
    """Create a simple table component."""
    return rx.table.body(
        rx.foreach(
            SimpleTableState.data,
            lambda row, index: simple_table_row(index),
        ),
        id="simple-table-body",
    )


def new_button() -> rx.Component:
    """Create a new button for the simple table."""
    return rx.button(
        rx.icon("plus", size=20),
        "Novo",
        id="simple-table-new-record-button",
        color_scheme="grass",
        on_click=SimpleTableState.handle_create_record,
    )


def simple_table_component(
    title: str | None = None,
    columns: list[dict[str, str | int | float]] | None = None,
    height: str | None = None,
) -> rx.Component:
    """Create a simple table component."""
    return rx.vstack(
        simple_table_title(title=title),
        rx.table.root(
            simple_table_header(columns=columns),
            simple_table_body(),
            width="100%",
            height="100%",
            class_id="simple-table",
            size="1",
            id="simple-table-root",
            border="1px solid green",
        ),
        height=height or "90vh",
        border="1px solid white",
        padding="0",
        spacing="0",
    )
