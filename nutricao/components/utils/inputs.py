#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Component for the application."""

import reflex as rx


def intersect(to_dict: dict, **props) -> dict:
    """merge dict"""
    to_dict |= {k: props[k] for k in props if k in to_dict}
    return to_dict


def commom_label(label: str = "", **props):
    """commom label for inputs"""
    label_props = {
        "size": "2",
        "weight": "medium",
        "text_align": "left",
        "width": "100%",
    }
    label_props = intersect(label_props, **props)
    return rx.text(label, **label_props)


def common_input(label_name: str = "", icon: rx.Component | None = None, **props) -> rx.Component:
    """commom input"""
    input_props = {
        "id": "name",
        "name": "name",
        "size": "2",
        "width": "100%",
        "required": True,
        "max_length": 128,
        "auto_focus": True,
        "type": "text",
        "placeholder": "",
    }
    input_props = intersect(input_props, **props)
    return rx.vstack(
        commom_label(label_name, **props),
        rx.input(rx.cond(icon, rx.input.slot(icon)), **input_props),
        spacing="0",
        justify="start",
        width="100%",
    )


def common_name_input(**props) -> rx.Component:
    """Name input component."""
    props["name"] = "name"
    props["id"] = "name"
    return (common_input("Nome", rx.icon("user"), **props),)


def common_identification_input(**props) -> rx.Component:
    """CPF input component."""
    props["name"] = "cpf"
    props["id"] = "cpf"
    return (common_input("CPF", rx.icon("user"), **props),)


def common_birthdate_input(**props) -> rx.Component:
    """CPF input component."""
    props["name"] = "birthdate"
    props["id"] = "birthdate"
    props["type"] = "date"
    return common_input("Data de Nascimento", None, **props)


def common_nickname_input(**props) -> rx.Component:
    """CPF input component."""
    props["name"] = "nickname"
    props["id"] = "nickname"
    props["max_length"] = 32
    props["placeholder"] = "Como gostaria de ser chamado"
    return common_input("Apelido", None, **props)
