#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""init module form application"""

import nutricao


def add_routes(app):
    """Add routes to the app."""
    # pylint: disable=import-outside-toplevel, wrong-import-position, wrong-import-order, unused-import
    from nutricao.components.login import login_form
    from nutricao.components.index import index_form
    from nutricao.components.signup import signup_form, signup_ok_form
    from nutricao.components.reset_password import reset_password_form, forgot_password_form
    from nutricao.components.utils import sidebar_bottom_profile, public_commom_form

    app.add_page(
        public_commom_form(None),
        route="/",
        title="Página Principal",
        description="Página Principal do Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        public_commom_form(login_form),
        route="/login",
        title="Login",
        description="Login do Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        public_commom_form(signup_form),
        route="/signup",
        title="Signup",
        description="Cadastro no Sistema",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        public_commom_form(signup_ok_form),
        route="/signup_ok",
        title="Confirmação do Cadastro",
        description="Confirmação do Cadastro",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        public_commom_form(reset_password_form),
        route="/reset_password",
        title="Resetar a Senha",
        description="Resetar a senha",
        image="https://reflex.dev/logo.png",
    )
    app.add_page(
        public_commom_form(forgot_password_form),
        route="/forgot_password",
        title="Recuperar a Senha",
        description="Recuperar a senha",
        image="https://reflex.dev/logo.png",
    )
