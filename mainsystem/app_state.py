#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, missing-class-docstring, missing-function-docstring, logging-fstring-interpolation
"""init module form application"""

import logging
from typing import Optional
import reflex as rx
from entities import User


class AppState(rx.State):
    """Application state class."""

    # Define the state variables
    current_user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_nickname: Optional[str] = None
    current_page: Optional[str] = None
    user_role: Optional[str] = None
    theme: str = "dark"  # Default theme is dark
    _logger = logging.getLogger("mainsystem")

    def clear_state(self):
        """Clear the application state."""
        self.current_user_id = None
        self.user_name = None
        self.user_email = None
        self.user_nickname = None
        self.current_page = None
        self.user_role = "guest"

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "dark" if self.theme == "light" else "light"
        self._logger.info(f"Theme changed to {self.theme}")

    def authenticate_user(self, user: User, role: str | None = None):
        """Authenticate user and set their role."""
        if user is None or user.id <= 0:
            self._logger.error("Invalid user ID for authentication")
            raise ValueError("Invalid user ID for authentication")
        self.current_user_id = user.id
        self.user_role = role or "guest"
        self.current_user_id = user.id
        self.user_name = user.name
        self.user_email = user.email
        self.user_nickname = user.first_name
        self._logger.info(f"User {self.current_user_id} authenticated as {role}")

    @rx.event
    def logout_user(self):
        """Logout user and reset state."""
        self.clear_state()
        self.user_role = "guest"
        self._logger.info(f"User {self.current_user_id} logged out")
        return rx.redirect("/")

    @rx.var
    def is_authenticated(self) -> bool:
        """Check if a user is authenticated."""
        return self.current_user_id is not None and self.current_user_id > 0

    @rx.var
    async def is_logged_in(self) -> bool:
        """compatibility with old versions of old systems"""
        return self.is_authenticated
