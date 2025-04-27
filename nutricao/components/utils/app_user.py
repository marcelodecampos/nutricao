#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable
"""Application Logged User Model."""

from dataclasses import dataclass


@dataclass
class AppUser:
    """Application Logged User Model."""

    login_id: int
