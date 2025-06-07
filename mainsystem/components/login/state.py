#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-instance-attributes, too-many-arguments, too-many-locals, too-many-statements, line-too-long, invalid-name, logging-fstring-interpolation, inherit-non-class, logging-not-lazy
"""Application state module.
This module contains the state of the application,
including user information and other relevant data."""

import logging

import bcrypt
import reflex as rx
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from entities import Login
from mainsystem import AppState
from utils import is_valid_email

logger = logging.getLogger("mainsystem")


class LoginState(AppState):
    """The login state."""

    # Define the state variables

    @staticmethod
    async def find_login_by_document(db_session, form_data: dict) -> Login:
        """Find a user by their document."""
        # This is a placeholder implementation. Replace with actual logic to find a user by their document.
        identification: str = form_data.get("login_id", "")
        logger.debug(f"find_login_by_document {identification}")
        # Print out the handlers
        query_str = (
            "select id from users where email = :identification"
            if is_valid_email(identification)
            else "select id from person where cpf = :identification"
        )
        logger.debug(f"query_str: {query_str}")
        login_entity: Login = None
        ret_value = None
        try:
            query = text(query_str).bindparams(identification=identification)
            stmt = db_session.exec(query)
            resultset: int = stmt.one()
            logger.debug(f"user_id: {resultset}")
            login_entity = db_session.get(Login, resultset[0])
            logger.debug(f"Login: {login_entity}")
            ret_value = login_entity
            if not bcrypt.checkpw(
                form_data["password"].encode(),
                login_entity.password.encode(),
            ):
                logger.warning("Password mismatch for user %s", login_entity.user_id)
                login_entity.attempts += 1
                ret_value = None
            else:
                if login_entity.attempts > 0:
                    logger.debug("Resetting attempts for user %s", login_entity.user_id)
                    login_entity.attempts = 0
            db_session.commit()
        except NoResultFound:
            logger.debug("NoResultFound")
            db_session.rollback()
            ret_value = None
        return ret_value

    @rx.event
    async def logout(self):
        """Logout the user."""
        logger.debug("Logout User")
        return self.logout_user()

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Handle the form submission."""
        # This is a placeholder implementation. Replace with actual logic to handle form submission.
        logger.debug("handle_submit")
        with rx.session() as db_session:
            login_entity = await self.find_login_by_document(db_session, form_data)
            if not login_entity:
                msgerr = "Usuário ou senha inválidos."
                logger.warning(msgerr + " %s", form_data["login_id"])
                yield rx.toast.error(msgerr)
                return
            self.authenticate_user(
                login_entity.user,
                "guest",
            )
            yield rx.redirect("/")
