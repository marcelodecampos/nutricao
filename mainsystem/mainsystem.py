#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position, wrong-import-order, unused-import, import-outside-toplevel, not-callable
"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging
import reflex as rx
from .routes import add_routes

logger = logging.getLogger()

logger.debug("Initing the application")
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="sky",
        gray_color="sand",
    ),
)

add_routes(app)
