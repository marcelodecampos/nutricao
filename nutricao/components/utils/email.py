"""Component for the application."""

import reflex as rx


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
