#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation
"""init module for components."""

import logging
from pprint import pformat
import reflex as rx

from entities import Person
from nutricao.components.utils import (
    common_name_input as name,
    common_identification_input as identification,
    common_birthdate_input as birthdate,
    common_nickname_input as nickname,
)
from nutricao.components.select.title import title_options
from nutricao.components.select.gender import gender_options
from nutricao.components.select.marital_status import marital_status_options
from nutricao.components.select.education import education_options


class MyDataState(rx.State):
    """My Data State Event Class"""

    my_data: rx.Field[Person] = rx.field(Person())
    _logger = logging.getLogger()

    @rx.event
    def handle_init(self, current_user: int):
        """handle init (on mount)  event"""
        self._logger.debug(f"Current User: {current_user}")


def my_data():
    """my personal info data"""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading("Meus Dados", size="6", as_="h2", width="100%"),
                    justify="start",
                    direction="column",
                    spacing="4",
                    width="100%",
                ),
                rx.form(
                    rx.flex(
                        name(),
                        nickname(),
                        rx.hstack(
                            identification(),
                            birthdate(),
                        ),
                        rx.hstack(
                            gender_options(),
                            title_options(),
                        ),
                        rx.hstack(
                            education_options(),
                            marital_status_options(),
                        ),
                        rx.separator(),
                        rx.button(
                            "Salvas Alterações",
                            size="3",
                            width="100%",
                            type="submit",
                            id="login_button",
                            name="login_button",
                        ),
                        justify="start",
                        direction="column",
                        spacing="4",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                    # on_submit=LoginState.handle_submit,
                    prevent_default=True,
                    id="login_form",
                    name="login_form",
                    method="POST",
                    padding="0",
                ),
                spacing="1",
                width="100%",
            ),
            size="4",
            max_width="35em",
            width="35em",
            padding="1",
        ),
        width="100%",
        height="80vh",
        # padding="2em",
        on_mount=MyDataState.handle_init(1),
    )
