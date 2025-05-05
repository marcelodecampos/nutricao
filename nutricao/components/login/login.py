# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long
"""Login form component for the application."""

import reflex as rx
from .state import LoginState


def other_login_options() -> rx.Component:
    """Other login options component."""
    return rx.center(
        rx.tooltip(
            rx.icon_button(rx.icon(tag="facebook"), variant="soft", size="3"),
            content="Facebook",
        ),
        rx.tooltip(
            rx.icon_button(rx.icon(tag="github"), variant="soft", size="3"),
            content="Github",
        ),
        rx.tooltip(
            rx.icon_button(rx.icon(tag="chrome"), variant="soft", size="3"),
            content="Google",
        ),
        rx.tooltip(
            rx.icon_button(rx.icon(tag="twitter"), variant="soft", size="3", tooltip="Twitter"),
            content="Twitter",
        ),
        spacing="4",
        direction="row",
        width="100%",
    )


def email_input() -> rx.Component:
    """Email input component."""
    return rx.vstack(
        rx.text("Seu E-mail", size="3", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("user")),
            placeholder="user@reflex.dev",
            type="email",
            id="login_id",
            name="login_id",
            size="3",
            width="100%",
            required=True,
            text=LoginState.email,
        ),
        spacing="2",
        justify="start",
        width="100%",
    )


def password_input() -> rx.Component:
    """Password input component."""
    return rx.vstack(
        rx.hstack(
            rx.text("Senha", size="3", weight="medium"),
            rx.link("Esqueceu a senha?", href="/forgot_password", size="3"),
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


def login_form() -> rx.Component:
    """Login form component."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading("Entrar na sua conta", size="6", as_="h2", width="100%"),
                    rx.hstack(
                        rx.text("Novo por aqui?", size="3", text_align="left"),
                        rx.link("Inscreva-se", href="/signup", size="3"),
                        spacing="2",
                        opacity="0.8",
                        width="100%",
                    ),
                    justify="start",
                    direction="column",
                    spacing="4",
                    width="100%",
                ),
                rx.form(
                    rx.flex(
                        email_input(),
                        password_input(),
                        rx.button(
                            "Entrar",
                            size="3",
                            width="100%",
                            type="submit",
                            id="login_button",
                            name="login_button",
                        ),
                        justify="start",
                        direction="column",
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    width="100%",
                    on_submit=LoginState.handle_submit,
                    prevent_default=True,
                    id="login_form",
                    name="login_form",
                    method="POST",
                ),
                rx.hstack(
                    rx.divider(margin="0"),
                    rx.text("Ou continue com", white_space="nowrap", weight="medium"),
                    rx.divider(margin="0"),
                    align="center",
                    width="100%",
                ),
                other_login_options(),
                spacing="6",
                width="100%",
            ),
            size="4",
            max_width="400px",
            width="100%",
        ),
        width="100%",
        height="100vh",
        #padding="2em",
    )
