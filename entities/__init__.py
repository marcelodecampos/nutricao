#!  python3
# -*- coding: utf-8 -*-
"""Entity modules"""

from .enums import ContDocID, PersonType
from .base import Base, SerialID, InsertUpdateDate, Name, UniqName, SimpleTable, IsValid
from .person import (
    ContactDocument,
    Gender,
    Title,
    User,
    Person,
    Company,
    MaritalStatus,
    Education,
    UserContactDocument,
)
from .places import Country, State, City
from .food import Food, FoodGroup, FoodComponent, FoodComposition
from .login import Login, LastUsedPasswords, LoginAudit
from .audit_log import AuditLog
from .access import Role, Permission, Resource
from .system import Menu


__all__ = [
    "ContDocID",
    "PersonType",
    "Base",
    "SerialID",
    "InsertUpdateDate",
    "IsValid",
    "Name",
    "UniqName",
    "SimpleTable",
    "ContactDocument",
    "Gender",
    "User",
    "Person",
    "Company",
    "Country",
    "State",
    "City",
    "Login",
    "Title",
    "MaritalStatus",
    "Education",
    "FoodGroup",
    "Food",
    "FoodComponent",
    "FoodComposition",
    "UserContactDocument",
    "AuditLog",
    "Role",
    "Permission",
    "Resource",
    "LastUsedPasswords",
    "LoginAudit",
    "Menu",
]

__version__ = "0.0.1"
