#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for gender conponent"""

import reflex as rx
from utils.logger import get_logger


LOGGER = get_logger("gender")


class GenderOptions(rx.State):
    """State class for gender options."""

    initial_values: list[tuple[str, str]] = []
    options: list[tuple[str, str]] = (
        ("0", "Prefixo não declarar"),
        ("1", "Masculino"),
        ("2", "Feminino"),
    )
    value = "0"

    def load_initial_values(self) -> None:
        """Load initial values."""
        LOGGER.debug("load gender from database")
        self.initial_values = (
            ("0", "Prefixo não declarar"),
            ("1", "Masculino"),
            ("2", "Feminino"),
        )


def gender_options() -> rx.Component:
    """gender combo box component."""
    LOGGER.debug("loading gender component")
    component = rx.vstack(
        rx.text("Qual seu Sexo", size="3", weight="medium", text_align="left", width="100%"),
        rx.select.root(
            rx.select.trigger(placeholder="No Selection"),
            rx.select.content(
                rx.select.group(
                    rx.foreach(
                        GenderOptions.options,
                        lambda x: rx.select.item(x[1], value=x[0]),
                    )
                ),
            ),
            value=GenderOptions.value,
            on_change=GenderOptions.set_value,
        ),
    )
    return component
