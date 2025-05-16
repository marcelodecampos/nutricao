#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-instance-attributes, too-many-arguments, too-many-locals, too-many-statements, line-too-long, invalid-name logging-fstring-interpolation inherit-non-class
"""Application state module.
This module contains the state of the application,
including user information and other relevant data."""

import logging
from dataclasses import dataclass
import bcrypt
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
    user: AppUser | None = None
    email: str = None

    @rx.var
    async def is_logged_in(self) -> bool:
        """Check if the user is logged in."""
        if self.user:
            str_name = self.user.name
        else:
            str_name = "NONE"
        logger.debug(f"self.user is {str_name}")
        return self.user is not None

    @staticmethod
    async def find_login_by_document(form_data: dict) -> Login:
        """Find a user by their document."""
        # This is a placeholder implementation. Replace with actual logic to find a user by their document.
        logger.debug("find_login_by_document")
        # Print out the handlers
        async with rx.asession() as db_session:
            query = (
                select(Login)
                .select_from(UserContactDocument)
                .join(Login, Login.user_id == UserContactDocument.user_id)
                .where(UserContactDocument.name == form_data["login_id"])
            )
            try:
                stmt = await db_session.exec(query)
                resultset = stmt.one()
                login_entity = resultset[0]
                await db_session.commit()
                if not bcrypt.checkpw(
                    form_data["password"].encode(), login_entity.password.encode()
                ):
                    logger.debug("bcrypt failed")
                    return None
                return login_entity
            except NoResultFound:
                logger.debug("NoResultFound")
                db_session.rollback()
                return None

    @rx.event(background=True)
    async def logout(self):
        """Logout the user."""
        logger.debug("Logout User")
        async with self:
            self.user = None
        yield rx.redirect("/")

    @rx.event(background=True)
    async def handle_submit(self, form_data: dict):
        """Handle the form submission."""
        # This is a placeholder implementation. Replace with actual logic to handle form submission.
        logger.debug("handle_submit")
        async with self:
            login_entity: Login = await self.find_login_by_document(form_data)
            if login_entity:
                self.user = AppUser(
                    login_id=login_entity.user_id,
                    name=login_entity.user.name,
                    email=login_entity.user.email,
                    first_name=login_entity.user.first_name,
                )
                yield rx.redirect("/")
            else:
                yield rx.toast.error("Usuário ou senha inválidos.")
