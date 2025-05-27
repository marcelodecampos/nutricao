#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""init file for utils module."""

import reflex as rx
from mainsystem import AppState


def user_info_ly():
    """Commom user info layout"""
    return rx.hstack(
        rx.icon_button(
            rx.icon("user"),
            size="3",
            radius="full",
        ),
        rx.vstack(
            rx.box(
                rx.text(
                    AppState.user_nickname,
                    size="2",
                    weight="medium",
                ),
                rx.text(
                    AppState.user_email,
                    size="2",
                    weight="medium",
                ),
                width="100%",
            ),
            spacing="0",
            align="start",
            justify="start",
            width="100%",
        ),
        padding_x="0.5rem",
        align="center",
        justify="start",
        width="100%",
    )


def user_info_options():
    """Commom user info layout options"""
    return rx.menu.root(
        rx.menu.trigger(
            user_info_ly(),
        ),
        rx.menu.content(
            rx.menu.item("Meus Dados", on_click=rx.redirect("/users/my_data")),
            rx.menu.item("Alterar Senha"),
            rx.menu.separator(),
            rx.menu.item("Sair do sistema", on_click=AppState.logout_user),
        ),
    )
