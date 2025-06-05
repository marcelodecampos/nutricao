#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, pointless-string-statemen, unnecessary-lambda
import reflex as rx


def delete_users_dialog(config: dict) -> rx.Component:
    """Creates a dialog for deleting users."""
    if not config:
        raise ValueError("Config dictionary cannot be empty.")
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(button_label, color_scheme="red"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(dialog_title),
            rx.alert_dialog.description(
                "Tem certeza que deseja apagar estas informações? Esta ação não pode ser desfeita!",
                size="2",
            ),
            rx.inset(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.foreach(
                                columns,
                                lambda col: rx.table.column_header_cell(col),
                            ),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            rows,
                            lambda row: rx.table.row(
                                rx.foreach(
                                    row,
                                    lambda cell: rx.table.cell(cell),
                                ),
                            ),
                        ),
                    ),
                ),
                side="x",
                margin_top="24px",
                margin_bottom="24px",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(button_label, color_scheme="red"),
                ),
                spacing="3",
                justify="end",
            ),
            style={"max_width": 500},
        ),
    )
