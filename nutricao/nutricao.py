#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging

import reflex as rx

# pylint: disable=wrong-import-position, wrong-import-order, unused-import, import-outside-toplevel
from .routes import add_routes

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.INFO)

for handler in sqlalchemy_logger.handlers:
    handler.setLevel(logging.INFO)


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="grass",
    ),
)

add_routes(app)
