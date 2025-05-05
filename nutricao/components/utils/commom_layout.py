#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""module file for commom layout."""
from types import FunctionType
from entities.login import Login
from nutricao.components.login.state import LoginState
import reflex as rx

def logout_item(text: str, icon: str) -> rx.Component:
    """Create a sidebar item with an icon and text."""
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
            on_click=LoginState.logout,
        ),
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    """Create a sidebar item with an icon and text."""
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    """Create a list of sidebar items."""
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def desktop_sidebar() -> rx.Component:
    """Create a sidebar profile section."""
    return rx.desktop_only(
        rx.vstack(
            rx.hstack(
                rx.image(
                    src="/dietista.png",
                    width="2.25em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading("MinhaNutri", size="4", weight="bold"),
                align="center",
                justify="start",
                padding_x="0.5rem",
                width="100%",
            ),
            sidebar_items(),
            rx.spacer(),
            rx.vstack(
                rx.vstack(
                    sidebar_item("Settings", "settings", "/#"),
                    logout_item("Log out", "log-out"),
                    spacing="1",
                    width="100%",
                ),
                rx.divider(),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("user"),
                        size="3",
                        radius="full",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text(
                                LoginState.user.first_name,
                                size="2",
                                weight="medium",
                            ),
                            rx.text(
                                LoginState.user.email,
                                size="2",
                                weight="medium",
                            ),
                            width="100%",
                        ),
                        spacing="0",
                        align="start",
                        justify="start",
                        width="100%",
                    ),
                    padding_x="0.5rem",
                    align="center",
                    justify="start",
                    width="100%",
                ),
                width="100%",
                spacing="5",
            ),
            spacing="5",
            # position="fixed",
            # left="0px",
            # top="0px",
            # z_index="5",
            padding_x="1em",
            padding_y="1.5em",
            bg=rx.color("accent", 3),
            align="start",
            # height="100%",
            height="650px",
            width="16em",
        ),
    )


def mobile_sidebar() -> rx.Component:
    """Create a sidebar profile section."""
    return rx.mobile_and_tablet(
        rx.drawer.root(
            rx.drawer.trigger(rx.icon("align-justify", size=30)),
            rx.drawer.overlay(z_index="5"),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.box(
                            rx.drawer.close(rx.icon("x", size=30)),
                            width="100%",
                        ),
                        sidebar_items(),
                        rx.spacer(),
                        rx.vstack(
                            rx.vstack(
                                sidebar_item(
                                    "Settings",
                                    "settings",
                                    "/#",
                                ),
                                sidebar_item(
                                    "Log out",
                                    "log-out",
                                    "/#",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.divider(margin="0"),
                            rx.hstack(
                                rx.icon_button(
                                    rx.icon("user"),
                                    size="3",
                                    radius="full",
                                ),
                                rx.vstack(
                                    rx.box(
                                        rx.text(
                                            "My account",
                                            size="3",
                                            weight="bold",
                                        ),
                                        rx.text(
                                            "user@reflex.dev",
                                            size="2",
                                            weight="medium",
                                        ),
                                        width="100%",
                                    ),
                                    spacing="0",
                                    justify="start",
                                    width="100%",
                                ),
                                padding_x="0.5rem",
                                align="center",
                                justify="start",
                                width="100%",
                            ),
                            width="100%",
                            spacing="5",
                        ),
                        spacing="5",
                        width="100%",
                    ),
                    top="auto",
                    right="auto",
                    height="100%",
                    width="20em",
                    padding="1.5em",
                    bg=rx.color("accent", 2),
                ),
                width="100%",
            ),
            direction="left",
        ),
        padding="1em",
    )


def sidebar_bottom_profile() -> rx.Component:
    """Create a sidebar profile section."""
    return rx.box(
        desktop_sidebar(),
        mobile_sidebar(),
    )


def navbar_link(text: str, url: str) -> rx.Component:
    """Create a navbar link."""
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def navbar_icons_menu_item(text: str, icon: str, url: str) -> rx.Component:
    """Create a navbar item with an icon and text."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=32),
            rx.text(text, size="4", weight="medium"),
            align="center",
        ),
        href=url,
    )


def public_commom_form(callback:FunctionType) -> rx.Component:
    """Create a common form for public pages."""
    callback_result=rx.box()
    if callback is not None:
        callback_result = rx.box (callback())
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/dietista.png",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Minha Nutri", size="4", weight="bold"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_icons_menu_item("Home", "home", "/#"),
                    navbar_icons_menu_item("Sobre", "", "/#"),
                    navbar_icons_menu_item("Preços", "coins", "/#"),
                    navbar_icons_menu_item("Contato", "mail", "/#"),
                    spacing="5",
                ),
                rx.hstack(
                    navbar_icons_menu_item("Cadastre-se", "file-pen", "/signup"),
                    navbar_icons_menu_item("Entrar", "log-in", "/login"),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/dietista.png",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Minha Nutri", size="3", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Homexxx"),
                        rx.menu.item("Sobre"),
                        rx.menu.item("Preços"),
                        rx.menu.item("Contato"),
                        rx.menu.separator(),
                        rx.menu.item("Entrar"),
                        rx.menu.item("Cadastre-se"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        callback_result,
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )

def private_commom_form(callback:FunctionType) -> rx.Component:
    return rx.box(
        desktop_sidebar(),
        mobile_sidebar(),
    )

def commom_layout(callback:FunctionType) -> rx.Component:
    """Create a common layout for the app."""
    return rx.box(
        rx.cond(
            LoginState.is_logged_in,
            private_commom_form(callback),
            public_commom_form(callback),
        ),
    )