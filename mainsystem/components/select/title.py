#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for gender conponent"""

import logging
import reflex as rx
from sqlalchemy import select
from entities import Title
from .base import get_values_from_database, common_select_component


LOGGER = logging.getLogger("TitleSelectComponent")


def title_options(inputprops: dict | None) -> rx.Component:
    """title combo box component."""
    LOGGER.debug("loading title component")
    if not inputprops:
        inputprops = {}
    inputprops["name"] = "title_options"
    inputprops["id"] = "title_options"
    return common_select_component(
        get_values_from_database(select(Title).order_by(Title.name)),
        "Modo de tratamento",
        **inputprops,
    )
