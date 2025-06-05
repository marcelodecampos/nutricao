#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""multi select solumn - Should be the first column."""

from typing import Callable, Literal, Optional
import reflex as rx


def conditional_multi_select_head_cell(
    var_conditional,
    fn_all: Callable[[], None] | None,
    fn_invert: Callable[[], None] | None,
    fn_none: Callable[[], None] | None,
    **props,
) -> rx.Component:
    """Return the ID cell component for the simple table with conditional rendering."""
    return rx.cond(
        var_conditional,
        multi_select_head_cell(
            fn_all=fn_all,
            fn_invert=fn_invert,
            fn_none=fn_none,
            **props,
        ),
        None,
    )


def multi_select_head_cell(
    fn_all: Callable[[], None] | None,
    fn_invert: Callable[[], None] | None,
    fn_none: Callable[[], None] | None,
    width: str | None = None,
    variant: Optional[Literal["classic", "ghost", "outline", "soft", "solid", "surface"]] = None,
) -> rx.Component:
    """Return the ID cell component for the simple table."""
    return rx.table.column_header_cell(
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    "ID",
                    rx.icon("chevrons-down", size=20, stroke_width=1),
                    variant=variant or "soft",
                    size="1",
                    spacing="0",
                    padding="0",
                    border="none",
                    width="100%",
                    height="100%",
                    id="simple-table-id-column-header-button",
                ),
            ),
            rx.menu.content(
                rx.menu.item("Todos", on_click=fn_all),
                rx.menu.item("Inverter", on_click=fn_invert),
                rx.menu.item("Nenhum", on_click=fn_none),
            ),
        ),
        width=width or "50px",
        spacing="0",
        padding="0",
        id="simple-table-header-id-cell",
        border="1px solid rgb(100, 100, 100)",
    )


def conditional_row_select_cell(
    var_conditional,
    index: int,
    items: dict[int, bool],
    fn_on_change: Callable[[rx.Var[bool], int], None] | None = None,
    width: str | None = None,
    **props,
) -> rx.Component:
    """Return the ID cell component for the simple table with conditional rendering."""
    return rx.cond(
        var_conditional,
        row_select_cell(
            index=index,
            items=items,
            fn_on_change=fn_on_change,
            width=width,
            **props,
        ),
        None,
    )


def row_select_cell(
    index: int,
    items: dict[int, bool],
    fn_on_change: Callable[[rx.Var[bool], int], None] | None = None,
    width: str | None = None,
) -> rx.Component:
    """Create a simple table component."""
    return rx.table.cell(
        rx.checkbox(
            id="simple-table-cell-checkbox-{index}",
            checked=items.get(index, False),
            on_change=(lambda value: fn_on_change(value, index)) if fn_on_change else None,
        ),
        id="simple-table-cell-{index}",
        border="1px solid rgb(100, 100, 100)",
        width=width or "50px",
    )
