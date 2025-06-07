#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import reflex as rx

from .h_cell import head_cell


def simple_table_header(columns: list[dict[str, str]] | None = None) -> rx.Component:
    """Create a simple table header component.

    Returns:
        rx.Component: A component representing the table header.
    """
    if not columns:
        columns = [
            {"label": "Column 1"},
        ]
    return rx.table.header(
        rx.table.row(
            rx.foreach(
                columns,
                lambda header_column, index: head_cell(index, header_column),
            ),
        ),
    )
