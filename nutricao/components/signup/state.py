# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long, inherit-non-class, broad-exception-caught
import json

import reflex as rx
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from entities import AuditLog, Login, UserContactDocument, Person, ContactDocument


class SignupFormState(rx.State):
    """State for the signup form."""

    password: str = ""
    confirm_password: str = ""

    email: str = ""
    confirm_email: str = ""

    is_loading: bool = False

    def _store_audit(self, db_session, json_data: str) -> bool:
        """Store audit log in the database."""
        # Create a new AuditLog entry
        try:
            audit_log = AuditLog(action="signup", target_data=json_data)
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

    def _exists_email_or_cpf_on_database(self, db_session, form_data: dict) -> bool:
        """Verify if the fields are valid."""
        # Check if the fields are valid (e.g., not empty, valid format)
        # You can implement your own validation logic here
        if self._exists_document(
            db_session,
            form_data["cpf"],
        ) or self._exists_document(
            db_session,
            form_data["login_id"],
        ):
            return True
        return False

    def _verify_password(self, form_data: dict) -> bool:
        """Verify if the password and confirm password match."""
        return form_data["password"] == form_data["confirmPassword"]

    def _verify_email(self, form_data: dict) -> bool:
        """Verify if the email and confirm email match."""
        return form_data["login_id"] == form_data["confirmEmail"]

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
        except Exception:
            return False

    @rx.event
    def on_submit(self, form_data: dict) -> rx.event.EventSpec:
        """Handle form submission."""
        # Handle form submission logic here
        # For example, you can access the form data using event.target.elements
        # and perform any necessary actions (e.g., sending data to a server)
        if not self._verify_password(form_data):
            return rx.toast.error("As senhas não coincidem.")
        if not self._verify_email(form_data):
            return rx.toast.error("Os e-mails não coincidem.")
        with rx.session() as db_session:
            # Create a new AuditLog entry
            if not self._exists_email_or_cpf_on_database(db_session, form_data):
                if self._add_new_user(db_session, form_data):
                    if self._store_audit(db_session, json.dumps(form_data)):
                        self.is_loading = True
                        db_session.commit()
                        return rx.redirect("/signup_ok")
                    else:
                        return rx.toast.error("Erro ao armazenar o log de auditoria.")
                else:
                    return rx.toast.error("Erro ao criar o usuário.")
            else:
                return rx.toast.error("CPF ou e-mail já cadastrado.")

    @rx.event
    def verify_password(self) -> rx.event.EventSpec | None:
        """Verify if the password and confirm password match."""
        if self.password != self.confirm_password:
            return rx.toast.error("As senhas não coincidem.")

    @rx.event
    def verify_email(self) -> rx.event.EventSpec | None:
        """Verify if the email and confirm email match."""
        if self.email != self.confirm_email:
            return rx.toast.error("Os e-mails não coincidem.")

    def on_load(self):
        """Handle form load."""
        self.password: str = ""
        self.confirm_password: str = ""

        self.email: str = ""
        self.confirm_email: str = ""

        self.is_loading: bool = False
