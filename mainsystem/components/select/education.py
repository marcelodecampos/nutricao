#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, inherit-non-class
"""module for education conponent"""

import logging
import reflex as rx
from sqlalchemy import select
from entities import Education
from .base import get_values_from_database, common_select_component


LOGGER = logging.getLogger("EducationSelectComponent")


def education_options(inputprops: dict | None) -> rx.Component:
    """education combo box component."""
    LOGGER.debug("loading education component")
    if not inputprops:
        inputprops = {}
    inputprops["name"] = "education_options"
    inputprops["id"] = "education_options"

    component = common_select_component(
        get_values_from_database(select(Education).order_by(Education.id)),
        "Grau de Instrução",
        **inputprops,
    )
    return component
