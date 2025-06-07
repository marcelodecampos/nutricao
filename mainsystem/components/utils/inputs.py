#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Component for the application."""

import reflex as rx


def input_label_component(
    label: str | None = None,
    show_link: bool = False,
    link_href: str | None = None,
    link_text: str | None = None,
    size: str = "2",
) -> rx.Component:
    """common label for common inputs"""
    commom_props = {
        "size": size or "2",
        "weight": "medium",
        "text_align": "left",
        "padding": "0",
        "spacing": "0",
    }
    return rx.cond(
        show_link,
        rx.hstack(
            rx.text(
                label or "Label",
                width="100%",
                **commom_props,
            ),
            rx.link(
                link_text or "Link",
                href=link_href or "#",
                width="100%",
                size=commom_props.get("size", "1"),
                justify="end",
                text_align="right",
            ),
            justify="between",
            **commom_props,
            width="100%",
        ),
        rx.text(
            label or "Label",
            width="100%",
            **commom_props,
        ),
    )


def input_component(
    label: str | None = None,
    icon: rx.Component | None = None,
    html_id: str | None = None,
    html_name: str | None = None,
    required: bool = False,
    max_length: int = 128,
    input_type: str = "text",
    placeholder: str = "Insira um valor",
    **props: dict | None,
) -> rx.Component:
    """commom input"""
    return rx.vstack(
        input_label_component(label, size="2", **props),
        rx.input(
            rx.cond(icon, rx.input.slot(icon)),
            id=html_id or "input_name",
            name=html_name or html_id or "input_name",
            size="2",
            width="100%",
            required=required,
            max_length=max_length,
            type=input_type,
            placeholder=placeholder,
            padding="0",
            spacing="0",
        ),
        justify="start",
        width="100%",
        spacing="1",
    )


def intersect(to_dict: dict, **props) -> dict:
    """merge dict"""
    to_dict |= {k: props[k] for k in props if k in to_dict}
    return to_dict


def commom_label(label: str = "", **props):
    """commom label for inputs"""
    label_props = {
        "size": "1",
        "weight": "medium",
        "text_align": "left",
        "width": "100%",
        "padding": "0",
        "spacing": "0",
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
        "size": "1",
        "width": "100%",
        "required": True,
        "max_length": 128,
        "auto_focus": True,
        "type": "text",
        "placeholder": "",
        "padding": "0",
        "spacing": "0",
    }
    input_props = input_props | inputprops
    return rx.vstack(
        commom_label(label_name, **labelprops),
        rx.input(
            rx.cond(icon, rx.input.slot(icon)),
            **input_props,
        ),
        justify="start",
        width="100%",
        padding="0.3rem",
        spacing="0",
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
    inputprops["required"] = False
    return common_input(inputprops, labelprops, label_name="Data de Nascimento")


def common_nickname_input(
    inputprops: dict | None = None,
    labelprops: dict | None = None,
) -> rx.Component:
    """Nickname input component."""
    if not inputprops:
        inputprops = {}
    if not labelprops:
        labelprops = {}
    inputprops["name"] = "nickname"
    inputprops["id"] = "nickname"
    inputprops["max_length"] = 32
    inputprops["placeholder"] = "Como gostaria de ser chamado"
    inputprops["required"] = False
    return input_component(label="Apelido")


def nickname_input() -> rx.Component:
    """Nickname input component."""
    return input_component(
        label="Apelido",
        html_id="id_nickname",
        html_name="input_nickname",
        max_length=32,
        placeholder="Como gostaria de ser chamado",
    )


def birthdate_input() -> rx.Component:
    """Data de Nascimento input component."""
    return input_component(
        label="Data de Nascimento",
        html_id="id_birthdate",
        html_name="input_birthdate",
        input_type="date",
    )


def identification_input() -> rx.Component:
    """CPF input component."""
    return input_component(
        label="CPF",
        html_id="id_cpf",
        html_name="input_cpf",
        placeholder="Insira seu CPF",
    )


def name_input() -> rx.Component:
    """Name input component."""
    return input_component(
        label="Nome",
        html_id="id_name",
        html_name="input_name",
        placeholder="Insira seu nome",
    )


def email_input() -> rx.Component:
    """Email input component."""
    return input_component(
        label="Seu E-mail",
        html_id="login_id",
        html_name="login_id",
        input_type="email",
        placeholder="user@email.com",
    )


def password_input(
    show_link: bool = False,
    link_href: str | None = None,
    link_text: str | None = None,
) -> rx.Component:
    """Password input component."""
    return input_component(
        label="Senha",
        html_id="id_password",
        html_name="password",
        input_type="password",
        placeholder="Entre com sua senha",
        icon=rx.input.slot(rx.icon("lock")),
        show_link=show_link,
        link_href=link_href,
        link_text=link_text,
    )
