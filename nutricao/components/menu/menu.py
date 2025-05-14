# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""init module for login component."""

from types import FunctionType
import reflex as rx


def menu_layout(callback: FunctionType | None = None) -> rx.Component:
    """Create a common layout for the app."""
    return rx.accordion.root(
        rx.accordion.item(
            header="First Item",
            content="The first accordion item's content",
        ),
        rx.accordion.item(
            header="Second Item",
            content="The second accordion item's content",
        ),
        rx.accordion.item(
            header="Third item",
            content="The third accordion item's content",
        ),
        width="300px",
    )
