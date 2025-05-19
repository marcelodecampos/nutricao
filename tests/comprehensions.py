#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, missing-class-docstring, missing-function-docstring
"""comprehensions test module application"""

from pprint import pprint

label_props = {"size": "2", "weight": "medium", "text_align": "left", "width": "100%"}

all_props = {
    "placeholder": "name",
    "id": "name",
    "name": "name",
    "size": "2",
    "width": "13em",
    "required": True,
    "max_length": 128,
    "auto_focus": True,
    "spacing": "1",
    "justify": "start",
}

pprint(label_props)
label_props |= {k: all_props[k] for k in all_props if k in label_props}
pprint(label_props)
