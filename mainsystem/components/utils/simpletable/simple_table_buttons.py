#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""Simple table buttons for the simple table component."""

import reflex as rx


def new_button(button_label: str | None = None) -> rx.Component:
    """Create a new button for the simple table."""
    return rx.button(
        rx.icon("plus", size=20),
        button_label or "Novo",
        id="simple-table-new-record-button",
        color_scheme="grass",
        on_click=SimpleTableState.handle_create_record,
    )


def delete_button(title: str | None = None, button_label: str | None = None) -> rx.Component:
    """Create a delete button for the simple table."""

    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                rx.icon("minus", size=20),
                button_label or "Apagar",
                id="simple-table-delete-records-button",
                color_scheme="red",
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(title or "Apagar Registros"),
            rx.alert_dialog.description(
                "Tem certeza que deseja apagar estas informações? Esta ação não pode ser desfeita!",
                size="2",
            ),
        ),
    )
