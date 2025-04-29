# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long, inherit-non-class, broad-exception-caught
"""Login form component for the application."""

from enum import verify
import json

import reflex as rx
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from entities import AuditLog, Login, UserContactDocument, Person, ContactDocument


class SignupFormState(rx.State):
    """State for the signup form."""

    def _store_audit(self, db_session, json_data: str) -> bool:
        """Store audit log in the database."""
        # Create a new AuditLog entry
        try:
            audit_log = AuditLog(
                action="signup",
                target_data=json_data,
            )
            db_session.add(audit_log)
            return True
        except:
            return False

    def _exists_document(self, db_session, document: str) -> bool:
        """Check if the document already exists."""
        query = select(UserContactDocument).where(UserContactDocument.name == document)
        try:
            db_session.exec(query).one()
            return True
        except NoResultFound:
            return False

    def verify_password(self, form_data: dict) -> bool:
        """Verify if the password and confirm password match."""
        if form_data["password"] != form_data["confirmPassword"]:
            return False
        return True

    def verify_email(self, form_data: dict) -> bool:
        """Verify if the email and confirm email match."""
        if form_data["login_id"] != form_data["confirmEmail"]:
            return False
        return True

    def _exists_email_or_cpf_on_database(self, db_session, form_data: dict) -> bool:
        """Verify if the fields are valid."""
        # Check if the fields are valid (e.g., not empty, valid format)
        # You can implement your own validation logic here
        if self._exists_document(db_session, form_data["cpf"]) or self._exists_document(
            db_session, form_data["login_id"]
        ):
            return True
        return False

    def _add_new_user(self, db_session, form_data: dict) -> bool:
        """Add a new user to the database."""
        # Create a new user and add it to the database
        # You can implement your own logic to create a new user here
        try:
            new_person = Person(
                name=form_data["name"],
            )
            new_person.add(
                UserContactDocument(
                    contdoc=db_session.get(ContactDocument, 1),
                    name=form_data["cpf"],
                    is_main=True,
                )
            )
            new_person.add(
                UserContactDocument(
                    contdoc=db_session.get(ContactDocument, 10),
                    name=form_data["login_id"],
                    is_main=True,
                )
            )
            db_session.add(new_person)
            db_session.add(Login(user=new_person, password=form_data["password"]))
            return True
        except Exception as e:
            return False

    @rx.event
    async def on_submit(self, form_data: dict) -> None:
        """Handle form submission."""
        # Handle form submission logic here
        # For example, you can access the form data using event.target.elements
        # and perform any necessary actions (e.g., sending data to a server)
        with rx.session() as db_session:
            # Create a new AuditLog entry
            if not self._exists_email_or_cpf_on_database(db_session, form_data):
                if self._add_new_user(db_session, form_data):
                    if self._store_audit(db_session, json.dumps(form_data)):
                        db_session.commit()
                    else:
                        yield rx.toast.error("Erro ao armazenar o log de auditoria.")
                else:
                    yield rx.toast.error("Erro ao criar o usuário.")
            else:
                yield rx.toast.error("CPF ou e-mail já cadastrado.")
        # if not self.verify_password(form_data):
        #    yield rx.toast.error("As senhas são diferentes.")
        # elif not self.verify_email(form_data):
        #    yield rx.toast.error("Os e-mails são diferentes.")


def name_input() -> rx.Component:
    """Name input component."""
    return rx.vstack(
        rx.text("Qual seu Nome", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("user")),
            placeholder="Seu nome",
            id="name",
            name="name",
            size="1",
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
        rx.text("CPF", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("id-card")),
            placeholder="CPF",
            id="cpf",
            name="cpf",
            size="1",
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
        rx.text("Seu E-mail", size="2", weight="medium", text_align="left", width="100%"),
        rx.input(
            rx.input.slot(rx.icon("mail")),
            placeholder="E-mail",
            type="email",
            id="login_id",
            name="login_id",
            size="1",
            width="100%",
            required=True,
        ),
        rx.input(
            rx.input.slot(rx.icon("mail-check")),
            placeholder="Confirme seu e-mail",
            type="email",
            id="confirmEmail",
            name="confirmEmail",
            size="1",
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
            rx.text("Senha", size="2", weight="medium"),
            justify="between",
            width="100%",
        ),
        rx.input(
            rx.input.slot(rx.icon("lock")),
            placeholder="Entre com sua senha",
            type="password",
            name="password",
            id="password",
            size="1",
            width="100%",
            required=True,
        ),
        rx.input(
            rx.input.slot(rx.icon("lock-keyhole")),
            placeholder="Confirme a sua senha",
            type="password",
            name="confirmPassword",
            id="confirmPassword",
            size="1",
            width="100%",
            required=True,
        ),
        spacing="2",
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
                        "Cadastrar-se",
                        size="2",
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
                on_submit=SignupFormState.on_submit,
            ),
            spacing="6",
            width="100%",
        ),
        size="2",
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
