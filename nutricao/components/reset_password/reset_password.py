# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long, inherit-non-class, broad-exception-caught
"""Login form component for the application."""

import reflex as rx

from nutricao.components.signup.state import SignupFormState


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
        spacing="1",
        justify="start",
        width="100%",
    )


def password_input() -> rx.Component:
    """Password input component."""
    return rx.vstack(
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
    )


def reset_password_component() -> rx.Component:
    """Inner card component."""
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.heading("Reset de Senha", size="4", as_="h2", width="100%"),
            ),
            rx.form(
                rx.flex(
                    password_input(),
                    rx.button(
                        rx.spinner(loading=False),
                        "Atualizar a Senha",
                        size="2",
                        width="100%",
                        type="submit",
                        disabled=False,
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
            ),
            spacing="6",
            width="100%",
        ),
        size="2",
        max_width="35em",
        width="100%",
    )


def forgot_password_component() -> rx.Component:
    """Inner card component."""
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.heading("Reset de Senha", size="4", as_="h2", width="100%"),
            ),
            rx.form(
                rx.flex(
                    email_input(),
                    rx.button(
                        rx.spinner(loading=False),
                        "Enviar Solicitação de Recuperação",
                        size="2",
                        width="100%",
                        type="submit",
                        disabled=False,
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
            ),
            spacing="6",
            width="100%",
        ),
        size="2",
        max_width="35em",
        width="100%",
    )


def reset_password_form() -> rx.Component:
    """signup form component."""
    return rx.center(
        reset_password_component(),
        width="100%",
        height="100vh",
        padding="2em",
    )


def forgot_password_form() -> rx.Component:
    """signup ok form component."""
    return rx.center(
        forgot_password_component(),
        width="100%",
        height="100vh",
        padding="2em",
    )
