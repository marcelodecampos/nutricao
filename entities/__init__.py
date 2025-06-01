#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=pointless-string-statement
"""this is the init module for entities module"""

from .enums import ContDocID, PersonType
from .base import (
    Base,
    InsertDate,
    InsertUpdateDate,
    IsValid,
    Name,
    SerialID,
    SimpleTable,
    UniqName,
)
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
from .food import (
    Food,
    FoodGroup,
    FoodComponent,
    FoodComposition,
)
from .login import (
    Login,
    LastUsedPasswords,
    LoginAudit,
)
from .audit_log import AuditLog
from .access import Role, Permission, Resource
from .system import Menu
from .listeners import person_before_update_listener


"""
    KNOWN PROBLEMS THAT I HAVE WITH SQLMODEL

    GETTER properties simple does't work!!!!!!

    That error — cannot pickle 'classmethod' object — is a known issue when using @field_validator
    with SQLModel in certain contexts, especially when models are being used with multiprocessing,
    FastAPI, or SQLAlchemy ORM features that involve pickling.
    This happens because SQLModel (as of now) is still based on Pydantic v1, or is not fully
    compatible with all Pydantic v2 features, depending on the version you're using.

    In SQLModel, when you define a model with table=True (i.e., a database model),
    Pydantic validators (including @field_validator) are not called.

    This is a long-standing limitation due to how SQLModel integrates with SQLAlchemy

"""

__version__ = "0.0.1"
# Manual registry of all SQLAlchemy classes as a dict
SQLALCHEMY_CLASS_REGISTRY = {
    "AuditLog": AuditLog,
    "Base": Base,
    "City": City,
    "Company": Company,
    "ContactDocument": ContactDocument,
    "Country": Country,
    "Education": Education,
    "Food": Food,
    "FoodComponent": FoodComponent,
    "FoodComposition": FoodComposition,
    "FoodGroup": FoodGroup,
    "Gender": Gender,
    "InsertDate": InsertDate,
    "InsertUpdateDate": InsertUpdateDate,
    "IsValid": IsValid,
    "LastUsedPasswords": LastUsedPasswords,
    "Login": Login,
    "LoginAudit": LoginAudit,
    "MaritalStatus": MaritalStatus,
    "Menu": Menu,
    "Name": Name,
    "Permission": Permission,
    "Person": Person,
    "Resource": Resource,
    "Role": Role,
    "SerialID": SerialID,
    "SimpleTable": SimpleTable,
    "State": State,
    "Title": Title,
    "UniqName": UniqName,
    "User": User,
    "UserContactDocument": UserContactDocument,
}


__all__ = list(SQLALCHEMY_CLASS_REGISTRY.keys()) + [
    "ContDocID",
    "PersonType",
    "person_before_update_listener",
]
