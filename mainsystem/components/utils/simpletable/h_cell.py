#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

from typing import Optional, Literal
import reflex as rx


def head_cell(
    column_index: int,
    label: str | None,
    cell_width: str | None = None,
    variant: Optional[Literal["classic", "ghost", "outline", "soft", "solid", "surface"]] = None,
) -> rx.Component:
    """Return the ID cell component for the simple table."""
    return rx.table.column_header_cell(
        rx.button(
            label,
            variant=variant or "soft",
            size="1",
            spacing="0",
            padding="0",
            border="none",
            width="100%",
            height="100%",
            align="left",
            id=f"simple-table-column-header-cell-button-{column_index}",
        ),
        spacing="0",
        padding="0",
        id=f"simple-table-header-cell-{column_index}",
        border="1px solid rgb(100, 100, 100)",
        width=cell_width or "auto",
    )
