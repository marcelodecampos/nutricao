#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging

import reflex as rx

from nutricao.components.login import login_form
from nutricao.components.index import index_form
from nutricao.components.signup import signup_form, signup_ok_form


# Configure basic logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
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
app.add_page(signup_ok_form, route="/signup_ok")
app.add_page(signup_form, route="/signup")
app.add_page(login_form, route="/login")
app.add_page(index_form, route="/")
