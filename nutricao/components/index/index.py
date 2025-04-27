# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long
"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from nutricao.state.base_app_state import BaseAppState
from nutricao.components.login import login_form


def logged_index_form() -> rx.Component:
    """Welcome Page (Index)"""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


def index_form():
    """Index page component."""
    return rx.cond(
        BaseAppState.logged_in,
        logged_index_form(),
        login_form(),
    )
