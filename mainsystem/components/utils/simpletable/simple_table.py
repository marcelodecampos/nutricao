#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import reflex as rx

from .h_cell import head_cell
from .multi_select_column import (
    conditional_multi_select_head_cell,
    conditional_row_select_cell,
)
from .simple_table_buttons import delete_button
from .simple_table_state import SimpleTableState


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


def simple_table_component() -> rx.Component:
    """Create a simple table component."""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                SimpleTableState.title,
                class_id="simple-table-title",
                size="4",
                align="left",
                trim="both",
                width="100%",
                weight="light",
                id="simple-table-heading",
            ),
            rx.cond(
                SimpleTableState.is_multiple_select,
                (
                    new_button(),
                    delete_button(
                        on_click_callable=SimpleTableState.on_delete_selected_records,
                    ),  # type: ignore
                ),
                (new_button(),),
            ),
            width="100%",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    conditional_multi_select_head_cell(
                        SimpleTableState.multiple_select,
                        SimpleTableState.handle_id_select_all,  # type: ignore
                        SimpleTableState.handle_id_select_invert,  # type: ignore
                        SimpleTableState.handle_id_select_none,  # type: ignore
                    ),
                    rx.foreach(
                        SimpleTableState.columns,
                        lambda col, index: head_cell(
                            index,
                            col.get("label", col.get("field", "")),
                        ),
                    ),
                ),
                id="simple-table-header",
            ),
            simple_table_body(),
            width="100%",
            height="100%",
            class_id="simple-table",
            size="1",
            id="simple-table-root",
        ),
        height="100vh",
    )


def configure_columns() -> list[dict[str, str | int | float]]:
    """Configure the columns for the simple table."""
    columns: list[dict[str, str | int | float]] = [
        {
            "field": "formatted_cpf",
            "label": "CPF",
            "width": "110px",
        },
        {
            "field": "name",
            "label": "Nome",
        },
        {
            "field": "formatted_birthdate",
            "label": "Data de Nascimento",
            "width": "80px",
        },
        {
            "field": "age",
            "label": "Idade",
            "width": "40px",
            "type": "number",
            "justify": "end",
        },
        {
            "field": "email",
            "label": "Email",
        },
    ]
    SimpleTableState.columns = columns
    return columns


def test_simple_table() -> rx.Component:
    """Test the simple_table function."""

    return simple_table_component()
