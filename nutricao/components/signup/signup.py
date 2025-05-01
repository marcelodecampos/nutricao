# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long, inherit-non-class, broad-exception-caught
"""Login form component for the application."""

import reflex as rx

from nutricao.components.signup.state import SignupFormState


def name_input() -> rx.Component:
    """Name input component."""
    return rx.vstack(
        rx.text("Seu Nome", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("user")),
            placeholder="Seu nome",
            id="name",
            name="name",
            size="2",
            width="100%",
            required=True,
            max_length=128,
            auto_focus=True,
        ),
        spacing="1",
        justify="start",
        width="100%",
    )


def identification_input() -> rx.Component:
    """CPF input component."""
    return rx.vstack(
        rx.text("CPF", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("id-card")),
            placeholder="CPF",
            id="cpf",
            name="cpf",
            size="2",
            width="100%",
            required=True,
        ),
        spacing="1",
        justify="start",
        width="100%",
    )


def email_input() -> rx.Component:
    """Email input component."""
    return rx.vstack(
        rx.text("Seu E-mail", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("mail")),
            placeholder="E-mail",
            type="email",
            id="login_id",
            name="login_id",
            size="2",
            width="100%",
            required=True,
            on_change=SignupFormState.set_email,
        ),
        rx.input(
            rx.input.slot(rx.icon("mail-check")),
            placeholder="Confirme seu e-mail",
            type="email",
            id="confirmEmail",
            name="confirmEmail",
            size="2",
            width="100%",
            required=True,
            on_change=SignupFormState.set_confirm_email,
            on_blur=SignupFormState.verify_email,
        ),
        spacing="1",
        justify="start",
        width="100%",
    )


def password_input() -> rx.Component:
    """Password input component."""
    return rx.hstack(
        rx.vstack(
            rx.text("Senha", size="2", weight="medium"),
            rx.input(
                rx.input.slot(rx.icon("lock")),
                placeholder="Entre com sua senha",
                type="password",
                name="password",
                id="password",
                size="2",
                width="100%",
                required=True,
                on_change=SignupFormState.set_password,
            ),
            spacing="1",
            justify="start",
            width="100%",
        ),
        rx.vstack(
            rx.text("Confirme sua senha", size="2", weight="medium"),
            rx.input(
                rx.input.slot(rx.icon("lock-keyhole")),
                placeholder="Confirme a sua senha",
                type="password",
                name="confirmPassword",
                id="confirmPassword",
                size="2",
                width="100%",
                required=True,
                on_change=SignupFormState.set_confirm_password,
                on_blur=SignupFormState.verify_password,
            ),
            spacing="1",
            justify="start",
            width="100%",
        ),
        spacing="1",
        justify="start",
        width="100%",
    )


def innercard_component() -> rx.Component:
    """Inner card component."""
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.heading("Crie a sua conta", size="4", as_="h2", width="100%"),
            ),
            rx.form(
                rx.flex(
                    name_input(),
                    identification_input(),
                    email_input(),
                    password_input(),
                    rx.button(
                        rx.spinner(loading=SignupFormState.is_loading),
                        "Cadastrar-se",
                        size="2",
                        width="100%",
                        type="submit",
                        disabled=rx.cond(SignupFormState.is_loading, True, False),
                        id="signup_button",
                        name="signup_button",
                    ),
                    justify="start",
                    direction="column",
                    spacing="4",
                    width="100%",
                ),
                spacing="6",
                width="100%",
                id="signup_form",
                name="signup_form",
                method="POST",
                on_submit=SignupFormState.on_submit,
                on_mount=SignupFormState.on_load,
            ),
            spacing="6",
            width="100%",
        ),
        size="2",
        max_width="35em",
        width="100%",
    )


def signup_form() -> rx.Component:
    """signup form component."""
    return rx.center(
        innercard_component(),
        width="100%",
        height="100vh",
        padding="2em",
    )


def signup_ok_form() -> rx.Component:
    """signup ok form component."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading(
                        "Sua conta foi criada com sucesso!",
                        size="4",
                        as_="h2",
                        width="100%",
                    ),
                ),
                rx.flex(
                    rx.button(
                        "Voltar para o Login",
                        size="2",
                        width="100%",
                        on_click=rx.redirect("/"),
                    ),
                ),
                spacing="6",
                width="100%",
            ),
            size="2",
            max_width="35em",
            width="100%",
        ),
        width="100%",
        height="100vh",
        padding="2em",
    )
