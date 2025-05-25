#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Component for the application."""

import reflex as rx


def password_input() -> rx.Component:
    """Password input component."""
    return rx.vstack(
        rx.hstack(
            rx.text("Senha", size="3", weight="medium"),
            rx.link("Esqueceu a senha?", href="#", size="3"),
            justify="between",
            width="100%",
        ),
        rx.input(
            rx.input.slot(rx.icon("lock")),
            placeholder="Entre com sua senha",
            type="password",
            name="password",
            id="password",
            size="3",
            width="100%",
            required=True,
        ),
        spacing="2",
        width="100%",
    )
