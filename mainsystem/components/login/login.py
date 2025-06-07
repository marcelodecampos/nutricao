# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long
"""Login form component for the application."""

import reflex as rx

from ..utils import email_input, password_input
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
            rx.icon_button(
                rx.icon(tag="twitter"), variant="soft", size="3", tooltip="Twitter"
            ),
            content="Twitter",
        ),
        spacing="4",
        direction="row",
        width="100%",
    )


def login_form() -> rx.Component:
    """Login form component."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading("Entrar na sua conta", size="4", width="100%"),
                    rx.hstack(
                        rx.text("Novo por aqui?", size="2", text_align="left"),
                        rx.link("Inscreva-se", href="/signup", size="2"),
                        spacing="1",
                        opacity="0.8",
                        width="100%",
                    ),
                    justify="start",
                    direction="column",
                    spacing="1",
                    width="100%",
                ),
                rx.form(
                    rx.flex(
                        email_input(),
                        password_input(
                            show_link=True,
                            link_href="/forgot_password",
                            link_text="Esqueceu a senha?",
                        ),
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
            max_width="28em",
            width="100%",
        ),
        width="100%",
        height="80vh",
        # padding="2em",
    )
