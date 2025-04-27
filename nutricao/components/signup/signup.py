# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long
"""Login form component for the application."""

import reflex as rx
from nutricao.components.select.gender import gender_options


def name_input() -> rx.Component:
    """Name input component."""
    return rx.vstack(
        rx.text("Qual seu Nome", size="3", weight="medium", text_align="left", width="100%"),
        rx.select(
            ["Sr.", "Sra.", "Srta"],
            value="Sr.",
        ),
        rx.input(
            rx.input.slot(rx.icon("user")),
            placeholder="seu name",
            id="login_id",
            name="login_id",
            size="3",
            width="100%",
            required=True,
            min_length=10,
            max_length=128,
            auto_focus=True,
        ),
        spacing="2",
        justify="start",
        width="100%",
    )


def identification_input() -> rx.Component:
    """CPF input component."""
    return rx.vstack(
        rx.text("CPF", size="3", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("user")),
            placeholder="CPF",
            id="cpf",
            name="cpf",
            size="3",
            width="100%",
            required=True,
        ),
        spacing="2",
        justify="start",
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
        ),
        spacing="2",
        justify="start",
        width="100%",
    )


def birthdate_input() -> rx.Component:
    """Email input component."""
    return rx.vstack(
        rx.text("Data de Nascimento", size="3", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("cake")),
            placeholder="user@reflex.dev",
            type="date",
            id="birthdate",
            name="birthdate",
            size="3",
            width="100%",
            required=True,
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


def innercard_component() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.heading("Crie a sua conta", size="6", as_="h2", width="100%"),
            ),
            rx.form(
                rx.flex(
                    name_input(),
                    identification_input(),
                    email_input(),
                    gender_options(),
                    birthdate_input(),
                    rx.button(
                        "Cadastrar-se",
                        size="3",
                        width="100%",
                        type="submit",
                    ),
                    justify="start",
                    direction="column",
                    spacing="4",
                    width="100%",
                    id="signup_button",
                    name="signup_button",
                ),
                spacing="6",
                width="100%",
                id="signup_form",
                name="signup_form",
                method="POST",
            ),
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="35em",
        width="100%",
    )


def signup_form() -> rx.Component:
    """Login form component."""
    return rx.center(
        innercard_component(),
        width="100%",
        height="100vh",
        padding="2em",
    )
