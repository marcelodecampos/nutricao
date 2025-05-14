#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module, missing-function-docstring.html)
#
"""test module"""

import functools


@functools.cache
def create_function_from_name(name: str):
    print(f"Function '{name}' has been called!")
    try:
        functype = locals()[name]
        if not functype:
            functype = globals()[name]
    except KeyError:
        functype = globals()[name]
    return functype
    # dynamic_function.__name__ = name
    # return types.FunctionType(dynamic_function.__code__, globals(), name, params)
