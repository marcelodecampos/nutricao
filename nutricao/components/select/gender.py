#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for gender conponent"""

import logging
import reflex as rx
from sqlalchemy import select
from entities import Gender
from .base import get_values_from_database, common_select_component


LOGGER = logging.getLogger("GenderSelectComponent")


def gender_options(inputprops: dict | None) -> rx.Component:
    """gender combo box component."""
    LOGGER.debug("loading gender component")

    if not inputprops:
        inputprops = {}
    inputprops["name"] = "gender_options"
    inputprops["id"] = "gender_options"
    component = common_select_component(
        get_values_from_database(select(Gender).order_by(Gender.name)),
        "Qual seu sexo",
        **inputprops,
    )
    return component
