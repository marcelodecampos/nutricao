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


from mainsystem.components.utils import (
    common_name_input as name,
    common_identification_input as identification,
    common_birthdate_input as birthdate,
    common_nickname_input as nickname,
)
from mainsystem.components.select import (
    title_options,
    gender_options,
    marital_status_options,
    education_options,
)


from entities import Person, User, Gender


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

    current_user_id: int = 0

    _logger = logging.getLogger()

    def load_data_from_entity(self, current_user: User):
        """convert Login to Form vars"""
        if not current_user:
            raise ValueError("Login não pode ser vazio ou nulo")

        self.name: str = current_user.name
        self.nick_name: Optional[str] = current_user.nick_name
        self.birthdate: Optional[str] = str(current_user.birthdate)
        if isinstance(current_user, Person):
            self.gender_id: str = str(current_user.gender_id)
            self.education_id: str = str(current_user.education_id)
            self.marital_status_id: str = str(current_user.marital_status_id)
            self.title_id: str = str(current_user.title_id)
            self.identity = current_user.identity

    def save_data_into_entity(self, current_user: User):
        """convert Form vars to Login"""
        if not current_user:
            raise ValueError("Login não pode ser vazio ou nulo")

        current_user.name = self.name
        current_user.nick_name = self.nick_name
        current_user.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        if isinstance(current_user, Person):
            current_user.gender_id = self.gender_id
            current_user.education_id = self.education_id
            current_user.marital_status_id = self.marital_status_id
            current_user.title_id = self.title_id
            # current_user.identity = self.identity

    @rx.event
    async def handle_init(self, current_user_id: int):
        """handle init (on mount)  event"""
        self.current_user_id = current_user_id
        self._logger.debug(f"Current User: {current_user_id}")
        with rx.session() as db_session:
            query = select(User).where(User.id == current_user_id)
            stmt = db_session.scalars(query).unique()
            entity: User = stmt.one()
            self._logger.debug(f"Loaded entity: {type(entity)} - {str(entity)}")
            db_session.commit()
            self.load_data_from_entity(entity)

    @rx.event
    async def handle_submit(self, formdata: dict):
        """handle submit event"""
        self._logger.debug(f"Submit event: {formdata}")
        self._logger.debug(f"Submit event: {self}")
        with rx.session() as db_session:
            query = select(User).where(User.id == self.current_user_id)
            stmt = db_session.scalars(query).unique()
            entity: User = stmt.one()
            self._logger.debug(f"Loaded entity: {type(entity)} - {str(entity)}")
            self.save_data_into_entity(entity)
            db_session.commit()


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
            "Salvar Alterações",
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


def personal_data() -> rx.Component:
    """personal data form"""
    return rx.form(
        form_fields(),
        spacing="2",
        width="100%",
        # on_submit=LoginState.handle_submit,
        prevent_default=True,
        id="login_form",
        name="login_form",
        method="POST",
        padding="0",
        on_submit=MyDataState.handle_submit,
    )


def my_data() -> rx.Component:
    """my personal info data"""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Meus Dados", size="4", width="100%", align="center"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Pessoais", value="personal_data"),
                        rx.tabs.trigger("Documentos", value="documents"),
                        rx.tabs.trigger("Contatos", value="contacts"),
                    ),
                    rx.tabs.content(
                        personal_data(),
                        value="personal_data",
                        height="100%",
                        padding="0",
                        border_radius="0",
                        border_width="0",
                    ),
                    rx.tabs.content(
                        rx.text("item on tab 2"),
                        value="documents",
                        height="100%",
                        padding="0",
                        border_radius="0",
                        border_width="0",
                    ),
                    rx.tabs.content(
                        rx.text("item on tab 3"),
                        value="contacts",
                        height="100%",
                        padding="0",
                        border_radius="0",
                        border_width="0",
                    ),
                    default_value="personal_data",
                    spacing="1",
                    width="100%",
                    padding="0",
                    border_radius="0",
                    border_width="0",
                    border_color="transparent",
                    background_color="transparent",
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
