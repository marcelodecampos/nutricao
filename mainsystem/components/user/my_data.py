#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation
"""init module for components."""

import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import select
import reflex as rx
from faker import Faker
from mainsystem import AppState

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


from entities import Person, User


class MyDataState(AppState):
    """My Data State Event Class"""

    identity: Optional[str] = ""
    birthdate: Optional[str] = None
    gender_id: Optional[str] = None
    education_id: Optional[str] = None
    marital_status_id: Optional[str] = None
    title_id: Optional[str] = None

    _logger = logging.getLogger()

    def load_data_from_entity(self, current_user: User):
        """convert Login to Form vars"""
        if not current_user:
            raise ValueError("Login não pode ser vazio ou nulo")

        self.user_name: str = current_user.name
        self.user_nickname: Optional[str] = current_user.nick_name
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

        current_user.name = self.user_name
        current_user.nick_name = self.user_nickname
        current_user.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        if isinstance(current_user, Person):
            current_user.gender_id = self.gender_id
            current_user.education_id = self.education_id
            current_user.marital_status_id = self.marital_status_id
            current_user.title_id = self.title_id
            # current_user.identity = self.identity

    @rx.event
    async def handle_init(self):
        """handle init (on mount)  event"""
        if not self.current_user_id:
            yield rx.redirect("/")
            return
        self._logger.debug(f"Current User: {self.current_user_id}")
        with rx.session() as db_session:
            query = select(User).where(User.id == self.current_user_id)
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


def default_height(subtract: int = 0) -> str:
    """default height for components"""
    value = 300 - (subtract * 5 if subtract < 35 else 34)
    return f"f{value}"


def form_fields() -> rx.Component:
    """form fields component"""
    return rx.flex(
        name(
            inputprops=make_params(
                value=MyDataState.user_name,
                on_change=MyDataState.set_user_name,
            ),
        ),
        nickname(
            inputprops=make_params(
                value=MyDataState.user_nickname,
                on_change=MyDataState.set_user_nickname,
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
        rx.flex(
            rx.button(
                "Salvar Alterações",
                size="2",
                width="100%",
                type="submit",
                id="login_button",
                name="login_button",
                padding="0",
                spacing="0",
            ),
            padding="1rem",
            justify="center",
            width="100%",
        ),
        justify="start",
        direction="column",
        spacing="0",
        border="2px solid orange",
        width="100%",
    )


def personal_data() -> rx.Component:
    """personal data form"""
    return rx.form(
        form_fields(),
        width="100%",
        height="100%",
        prevent_default=True,
        id="login_form",
        name="login_form",
        method="POST",
        spacing="0",
        padding="0",
        on_submit=MyDataState.handle_submit,
    )


def documents() -> rx.Component:
    """Users documents table"""
    my_documents = []
    doc_type = [
        "CPF",
        "PASSAPORTE",
        "IDENTIDADE",
        "PIS/PASEP",
        "TIT. ELEITOR",
        "CERTIDÃO DE NASCIMENTO",
        "CNPJ",
    ]
    faker_data = Faker("pt_BR")
    for index in range(300):
        my_documents.append(
            {
                "Tipo": doc_type[faker_data.random_int(0, 6)],
                "Documento": faker_data.cpf(),
                "Principal": False if index % 5 == 0 else True,
            }
        )
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Tipo"),
                rx.table.column_header_cell("Documento"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                my_documents,
                lambda doc: rx.table.row(
                    rx.table.cell(doc["Tipo"]),
                    rx.table.cell(doc["Documento"]),
                    on_click=rx.toast.info("Ohhhhh!Yewsssss"),
                ),
            ),
        ),
        width="100%",
        height="395px",
        border="2px solid white",
    )


def contacts() -> rx.Component:
    """Users documents table"""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Tipo"),
                rx.table.column_header_cell("Contato"),
                rx.table.column_header_cell("Principal"),
            ),
        ),
        rx.table.body(
            rx.table.row(
                rx.table.row_header_cell("Danilo Sousa"),
                rx.table.cell("danilo@example.com"),
                rx.table.cell("Developer"),
            ),
            rx.table.row(
                rx.table.row_header_cell("Zahra Ambessa"),
                rx.table.cell("zahra@example.com"),
                rx.table.cell("Admin"),
            ),
            rx.table.row(
                rx.table.row_header_cell("Jasper Eriks"),
                rx.table.cell("jasper@example.com"),
                rx.table.cell("Developer"),
            ),
        ),
        width="100%",
        height="395px",
        border="2px solid white",
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
                        padding="0",
                        width="100%",
                        height="400px",
                        border="2px solid brown",
                    ),
                    rx.tabs.content(
                        documents(),
                        value="documents",
                        padding="0",
                        width="100%",
                        height="400px",
                        border="2px solid brown",
                    ),
                    rx.tabs.content(
                        contacts(),
                        value="contacts",
                        padding="0",
                        width="100%",
                        height="400px",
                        border="2px solid brown",
                    ),
                    default_value="personal_data",
                    width="100%",
                    height="450px",
                    border_radius="0",
                    border_color="transparent",
                    background_color="transparent",
                    border="2px solid blue",
                    max_height=default_height(3),
                    min_height=default_height(3),
                    padding="0",
                    spacing="0",
                ),
                width="100%",
                height="480px",
                overflow="auto",
                border="2px solid green",
                padding="0",
                spacing="0",
            ),
            size="4",
            max_width="35em",
            width="35em",
            height="495px",
            overflow="auto",
            padding="0",
            spacing="0",
            border="2px solid yellow",
        ),
        width="100%",
        height="500px",
        overflow="auto",
        # padding="2em",
        on_mount=MyDataState.handle_init,
        border="2px solid red",
    )
