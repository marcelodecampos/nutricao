#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for marital_status conponent"""

import reflex as rx
from sqlalchemy import select
from utils.logger import get_logger
from entities import MaritalStatus


LOGGER = get_logger("marital_status")


def __get_values_from_database() -> list[tuple[str, str]]:
    """Get values from database."""
    LOGGER.debug("getting marital_status values from database")
    values: list[tuple[str, str]] = []
    with rx.session() as db_session:
        query = select(MaritalStatus)
        resultset = db_session.exec(query)
        for entity in resultset.scalars().all():
            values.append((str(entity.id), entity.name))
    return values


def marital_status_options() -> rx.Component:
    """marital_status combo box component."""
    LOGGER.debug("loading marital_status component")
    values = __get_values_from_database()
    component = rx.vstack(
        rx.text("Estado Civil", size="2", weight="medium", text_align="left", width="100%"),
        rx.select.root(
            rx.select.trigger(placeholder="Selecione uma opção", width="100%"),
            rx.select.content(
                rx.foreach(
                    values,
                    lambda x: rx.select.item(x[1], value=x[0]),
                ),
                name="marital_status_options",
                id="marital_status_options",
            ),
        ),
        spacing="0",
        justify="start",
        width="100%",
    )
    return component
