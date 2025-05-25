#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for marital_status conponent"""

import logging
import reflex as rx
from sqlalchemy import select
from entities import MaritalStatus
from .base import get_values_from_database, common_select_component


LOGGER = logging.getLogger("MaritalStatusSelectComponent")


def marital_status_options(inputprops: dict | None) -> rx.Component:
    """marital_status combo box component."""
    LOGGER.debug("loading marital_status component")
    if not inputprops:
        inputprops = {}
    inputprops["name"] = "marital_status_options"
    inputprops["id"] = "marital_status_options"
    component = common_select_component(
        get_values_from_database(select(MaritalStatus).order_by(MaritalStatus.name)),
        "Qual seu estado civil",
        **inputprops,
    )
    return component
