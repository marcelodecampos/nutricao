#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""simple table teste file for simple table."""

import reflex as rx

from .simple_table import simple_table_component


def configure_columns() -> list[dict[str, str | int | float]]:
    """Configure the columns for the simple table."""
    columns: list[dict[str, str | int | float]] = [
        {
            "field": "formatted_cpf",
            "label": "CPF",
            "width": "110px",
        },
        {
            "field": "name",
            "label": "Nome",
        },
        {
            "field": "formatted_birthdate",
            "label": "Data de Nascimento",
            "width": "120px",
        },
        {
            "field": "age",
            "label": "Idade",
            "width": "40px",
            "type": "number",
            "justify": "end",
        },
        {
            "field": "email",
            "label": "Email",
        },
    ]
    return columns


def test_simple_table() -> rx.Component:
    """Test the simple_table function."""

    return simple_table_component(
        title="Teste com Simple Table",
        columns=configure_columns(),
    )
