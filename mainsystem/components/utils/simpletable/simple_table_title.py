#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import reflex as rx


def simple_table_title(title: str | None = None) -> rx.Component:
    """Create a simple table title component.
    Args:
        title (str | None): The title of the table. Defaults to "Simple Table".
    Returns:
        rx.Component: A component representing the table title.
    """
    return (
        rx.hstack(
            rx.heading(
                title or "Simple Table",
                class_id="simple-table-title",
                size="4",
                align="center",
                width="100%",
                height="100%",
                id="simple-table-heading",
                border="1px solid orange",
            ),
            width="100%",
            height="2.2em",
            border="1px solid yellow",
        ),
    )
