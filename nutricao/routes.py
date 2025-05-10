#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""init module form application"""

import nutricao
import reflex as rx


def add_routes(app):
    """Add routes to the app."""
    # pylint: disable=import-outside-toplevel, wrong-import-position, wrong-import-order, unused-import
    from nutricao.components.login import login_form
    from nutricao.components.index import index_form
    from nutricao.components.signup import signup_form, signup_ok_form
    from nutricao.components.reset_password import reset_password_form, forgot_password_form
    from nutricao.components.utils import commom_layout
    from nutricao.components.menu import menu_layout

    app.add_page(
        commom_layout(None),
        route="/",
        title="Página Principal",
        description="Página Principal do Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        commom_layout(login_form),
        route="/login",
        title="Login",
        description="Login do Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        commom_layout(signup_form),
        route="/signup",
        title="Signup",
        description="Cadastro no Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        commom_layout(signup_ok_form),
        route="/signup_ok",
        title="Confirmação do Cadastro",
        description="Confirmação do Cadastro",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        commom_layout(reset_password_form),
        route="/reset_password",
        title="Resetar a Senha",
        description="Resetar a senha",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        commom_layout(forgot_password_form),
        route="/forgot_password",
        title="Recuperar a Senha",
        description="Recuperar a senha",
        image="https://reflex.dev/logo.png",
    )

    app.add_page(
        commom_layout(rx.theme_panel),
        route="/settings",
        title="Recuperar a Senha",
        description="Recuperar a senha",
        image="https://reflex.dev/logo.png",
    )

    app.add_page(
        menu_layout(),
        route="/test/menu",
        title="Menu",
        description="Menu Tests",
        image="https://reflex.dev/logo.png",
    )
