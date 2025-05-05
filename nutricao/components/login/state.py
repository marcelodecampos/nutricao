#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-instance-attributes, too-many-arguments, too-many-locals, too-many-statements, line-too-long, invalid-name logging-fstring-interpolation inherit-non-class
"""Application state module.
This module contains the state of the application,
including user information and other relevant data."""

import logging
from os import name
import bcrypt
from dataclasses import dataclass
import reflex as rx
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from entities import UserContactDocument, Login

logger = logging.getLogger("minhanutri.nutricao")

@dataclass
class AppUser:
    """Application Logged User Model."""

    login_id: int
    name: str = None
    email: str = None
    first_name: str = None


class LoginState(rx.State):
    """The app state."""

    # Define the state variables
    user: AppUser = None
    email: str = None
    password: str = None
    form_data: dict = None


    @rx.var
    def is_logged_in(self) -> bool:
        """Check if the user is logged in."""
        logger.debug("is_logged_in")
        return self.user is not None


    def find_login_by_document(self, document: str, password: str) -> Login:
        """Find a user by their document."""
        # This is a placeholder implementation. Replace with actual logic to find a user by their document.
        logger.debug("find_login_by_document")
        # Print out the handlers
        with rx.session() as db_session:
            print (type(db_session))
            print (db_session)
            query = (
                select(Login)
                .select_from(UserContactDocument)
                .join(Login, Login.user_id == UserContactDocument.user_id)
                .where(UserContactDocument.name == document)
            )
            try:
                resultset = db_session.exec(query).one()
                login_entity = resultset[0]
                if not bcrypt.checkpw(password.encode(), login_entity.password.encode()):
                    logger.debug("bcrypt failed")
                    return None
                return login_entity
            except NoResultFound:
                logger.debug("NoResultFound")
                return None

    def logout(self) -> None:
        """Logout the user."""
        logger.debug("Logout User")
        self.user = None
        return rx.redirect("/")

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submission."""
        # This is a placeholder implementation. Replace with actual logic to handle form submission.
        logger.debug("handle_submit")
        self.form_data = form_data
        login_entity:Login = self.find_login_by_document(form_data["login_id"], form_data["password"])
        if not login_entity:
            yield rx.toast.error("Usuário ou senha inválidos.")
            return
        self.user = AppUser(login_id = login_entity.user_id,
                            name = login_entity.user.name,
                            email = login_entity.user.email,
                            first_name =login_entity.user.first_name)
        return rx.redirect("/")
