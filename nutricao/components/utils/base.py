#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""module file for commom layout."""
from types import FunctionType
from nutricao.components.login.state import LoginState
import reflex as rx

def base_layout(callback:FunctionType) -> rx.Component:
    """Base Layout for the application."""
    callback_result=rx.box()
    if callback is not None:
        callback_result = rx.box (callback())
    return rx.box (
        north_layout(),
        callback_result,
        width="100%",
        height="100vh",
        padding="0",
        border="solid 1px",
    )


def north_layout() -> rx.Component:
    """North Layout for the application."""
    return rx.box (
        width="100%",
        height="10vh",
        padding="0",
        border="solid 1px",
        color="black",
    )