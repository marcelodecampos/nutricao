"""module sys_user.py
This module contains the state of the application,"""

from pydantic.dataclasses import dataclass


@dataclass
class SysUser:
    """Class to represent a system user."""

    id: int = None
    name: str = None
    email: str = None
    is_active: bool = True
    is_superuser: bool = False

    def __str__(self):
        return f"SysUser(id={self.id}, name={self.name}, email={self.email})"
