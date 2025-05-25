#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation
"""base module for select components"""

import logging
import reflex as rx

LOGGER = logging.getLogger("BaseSelectComponent")


def get_values_from_database(query) -> list[tuple[str, str]]:
    """Get values from database."""
    LOGGER.debug("getting values from database, using common query for simple tables")
    values: list[tuple[str, str]] = []
    first: bool = True
    with rx.session() as db_session:
        resultset = db_session.scalars(query)
        for entity in resultset.all():
            if first:
                LOGGER.debug(f"{type(entity)}")
                first = False
            values.append((str(entity.id), entity.name))
        db_session.commit()
    return values


def common_select_component(values, label: str, **inputprops) -> rx.Component:
    """common combo box component."""
    LOGGER.debug(f"loading common component. {values}")
    component = rx.vstack(
        rx.text(label, size="2", weight="medium", text_align="left", width="100%"),
        rx.select.root(
            rx.select.trigger(placeholder="Selecione uma opção", width="100%"),
            rx.select.content(
                rx.foreach(
                    values,
                    lambda x: rx.select.item(x[1], value=x[0]),
                )
            ),
            default_value="1",
            **inputprops,
        ),
        spacing="0",
        justify="start",
        width="100%",
    )
    return component
