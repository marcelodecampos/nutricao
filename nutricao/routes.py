#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel, wrong-import-position, wrong-import-order, unused-import, not-callable
"""init module form application"""

import reflex as rx
from nutricao.components.login import login_form
from nutricao.components.signup import signup_form, signup_ok_form
from nutricao.components.reset_password import reset_password_form, forgot_password_form
from nutricao.components.utils import commom_layout
from nutricao.components.menu import menu_layout


APP_ROUTES: list[dict] = [
    {
        "commom_layout": None,
        "route": "/",
        "title": "Página Principal",
        "description": "Página Principal do Sistema",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": login_form,
        "route": "/login",
        "title": "Login",
        "description": "Login do Sistema",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": signup_form,
        "route": "/signup",
        "title": "Signup",
        "description": "Cadastro no Sistema",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": signup_ok_form,
        "route": "/signup_ok",
        "title": "Confirmação do Cadastro",
        "description": "Confirmação do Cadastro",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": reset_password_form,
        "route": "/reset_password",
        "title": "Resetar a Senha",
        "description": "Página Principal do Sistema",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": forgot_password_form,
        "route": "/forgot_password",
        "title": "Recuperar a Senha",
        "description": "Recuperar a senha",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": rx.theme_panel,
        "route": "/settings",
        "title": "Configuração do Usuário",
        "description": "Configuração do Usuário do Sistema",
        "image": "https://reflex.dev/logo.png",
    },
    {
        "commom_layout": menu_layout,
        "route": "/test/menu",
        "title": "Menu",
        "description": "Teste de Menu",
        "image": "https://reflex.dev/logo.png",
    },
]


def add_routes(app: rx.App):
    """Add routes to the app."""

    for route_item in APP_ROUTES:
        component: rx.Component = commom_layout(route_item.pop("commom_layout"))
        route_item["component"] = component
        app.add_page(**route_item)
