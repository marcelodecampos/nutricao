#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation
"""init module for components."""

import logging
from datetime import datetime
from typing import Optional
import sqlmodel
from sqlalchemy import select
import reflex as rx


from nutricao.components.utils import (
    common_name_input as name,
    common_identification_input as identification,
    common_birthdate_input as birthdate,
    common_nickname_input as nickname,
)
from nutricao.components.select import (
    title_options,
    gender_options,
    marital_status_options,
    education_options,
)


from entities import Login, Person, User, Gender


class MyDataState(rx.State):
    """My Data State Event Class"""

    name: str = ""
    nick_name: Optional[str] = ""
    identity: Optional[str] = ""
    birthdate: Optional[str] = None
    gender_id: Optional[str] = None
    education_id: Optional[str] = None
    marital_status_id: Optional[str] = None
    title_id: Optional[str] = None

    _logger = logging.getLogger()

    def load_data_from_entity(self, entity: Login):
        """convert Login to Form vars"""
        if not entity:
            raise ValueError("Login não pode ser vazio ou nulo")

        current_user: User = entity.user
        self.name: str = current_user.name
        self.nick_name: Optional[str] = current_user.nick_name
        self.birthdate: Optional[str] = str(current_user.birthdate)
        if isinstance(current_user, Person):
            self.gender_id: str = str(current_user.gender_id)
            self.education_id: str = str(current_user.education_id)
            self.marital_status_id: str = str(current_user.marital_status_id)
            self.title_id: str = str(current_user.title_id)
            self.identity = current_user.identity

    @rx.event
    async def handle_init(self, current_user: int):
        """handle init (on mount)  event"""
        self._logger.debug(f"Current User: {current_user}")
        with rx.session() as db_session:
            query = select(Login).where(Login.user_id == current_user)
            stmt = db_session.scalars(query)
            entity: Login = stmt.one()
            db_session.commit()
            self.load_data_from_entity(entity)
        self._logger.debug(f"Default gender value: {self.gender_id}")


def make_params(**kwargs) -> dict:
    """make params for input components"""
    return kwargs


def select_label(label: str) -> rx.Component:
    """select label component"""
    return rx.text(
        label,
        size="2",
        weight="medium",
        text_align="left",
        width="100%",
    )


def form_fields() -> rx.Component:
    """form fields component"""
    return rx.flex(
        name(
            inputprops=make_params(
                value=MyDataState.name,
                on_change=MyDataState.set_name,
            ),
        ),
        nickname(
            inputprops=make_params(
                value=MyDataState.nick_name,
                on_change=MyDataState.set_nick_name,
            )
        ),
        rx.hstack(
            identification(
                inputprops=make_params(
                    value=MyDataState.identity,
                    on_change=MyDataState.set_identity,
                ),
            ),
            birthdate(
                inputprops=make_params(
                    value=MyDataState.birthdate,
                    on_change=MyDataState.set_birthdate,
                ),
            ),
        ),
        rx.hstack(
            gender_options(
                inputprops=make_params(
                    value=MyDataState.gender_id,
                    on_change=MyDataState.set_gender_id,
                ),
            ),
            title_options(
                inputprops=make_params(
                    value=MyDataState.title_id,
                    on_change=MyDataState.set_title_id,
                ),
            ),
        ),
        rx.hstack(
            education_options(
                inputprops=make_params(
                    value=MyDataState.education_id,
                    on_change=MyDataState.set_education_id,
                ),
            ),
            marital_status_options(
                inputprops=make_params(
                    value=MyDataState.marital_status_id,
                    on_change=MyDataState.set_marital_status_id,
                ),
            ),
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
    )


def my_data() -> rx.Component:
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
                    form_fields(),
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
