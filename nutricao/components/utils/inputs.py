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
    label_props = label_props | props
    return rx.text(label, **label_props)


def common_input(
    inputprops: dict,
    labelprops: dict,
    label_name: str = "",
    icon: rx.Component | None = None,
) -> rx.Component:
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
    input_props = input_props | inputprops
    return rx.vstack(
        commom_label(label_name, **labelprops),
        rx.input(
            rx.cond(icon, rx.input.slot(icon)),
            **input_props,
        ),
        spacing="0",
        justify="start",
        width="100%",
    )


def common_name_input(
    inputprops: dict | None = None,
    labelprops: dict | None = None,
) -> rx.Component:
    """Name input component."""
    if not inputprops:
        inputprops = {}
    if not labelprops:
        labelprops = {}
    inputprops["name"] = "name"
    inputprops["id"] = "input_name"
    return (
        common_input(
            inputprops=inputprops,
            labelprops=labelprops,
            label_name="Nome",
            icon=rx.icon("user"),
        ),
    )


def common_identification_input(
    inputprops: dict | None = None,
    labelprops: dict | None = None,
) -> rx.Component:
    """CPF input component."""
    if not inputprops:
        inputprops = {}
    if not labelprops:
        labelprops = {}
    inputprops["name"] = "cpf"
    inputprops["id"] = "cpf"
    return common_input(inputprops, labelprops, label_name="CPF", icon=rx.icon("user"))


def common_birthdate_input(
    inputprops: dict | None = None,
    labelprops: dict | None = None,
) -> rx.Component:
    """CPF input component."""
    if not inputprops:
        inputprops = {}
    if not labelprops:
        labelprops = {}
    inputprops["name"] = "birthdate"
    inputprops["id"] = "birthdate"
    inputprops["type"] = "date"
    return common_input(inputprops, labelprops, label_name="Data de Nascimento")


def common_nickname_input(
    inputprops: dict | None = None,
    labelprops: dict | None = None,
) -> rx.Component:
    """CPF input component."""
    if not inputprops:
        inputprops = {}
    if not labelprops:
        labelprops = {}
    inputprops["name"] = "nickname"
    inputprops["id"] = "nickname"
    inputprops["max_length"] = 32
    inputprops["placeholder"] = "Como gostaria de ser chamado"
    return common_input(inputprops, labelprops, label_name="Apelido")
