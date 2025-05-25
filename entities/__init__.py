#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=pointless-string-statement
"""this is the init module for entities module"""

from .enums import ContDocID, PersonType
from .base import (
    Base,
    InsertDate,
    InsertDateModel,
    InsertUpdateDate,
    InsertUpdateDateModel,
    IsValid,
    IsValidModel,
    Name,
    NameModel,
    SerialID,
    SerialIDModel,
    SimpleTable,
    SimpleTableModel,
    UniqName,
    UniqNameModel,
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
    ContactDocumentModel,
    GenderModel,
    TitleModel,
    UserModel,
    PersonModel,
    CompanyModel,
    MaritalStatusModel,
    EducationModel,
    UserContactDocumentModel,
)
from .places import Country, State, City, CountryModel, StateModel, CityModel
from .food import (
    Food,
    FoodGroup,
    FoodComponent,
    FoodComposition,
    FoodModel,
    FoodGroupModel,
    FoodComponentModel,
    FoodCompositionModel,
)
from .login import (
    Login,
    LastUsedPasswords,
    LoginAudit,
    LoginModel,
    LastUsedPasswordsModel,
    LoginAuditModel,
)
from .audit_log import AuditLog, AuditLogModel
from .access import Role, Permission, Resource, RoleModel, PermissionModel, ResourceModel
from .system import Menu, MenuModel


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
__all__ = [
    "AuditLog",
    "AuditLogModel",
    "Base",
    "City",
    "CityModel",
    "Company",
    "CompanyModel",
    "ContactDocument",
    "ContactDocumentModel",
    "ContDocID",
    "Country",
    "CountryModel",
    "Education",
    "EducationModel",
    "Food",
    "FoodComponent",
    "FoodComponentModel",
    "FoodComposition",
    "FoodCompositionModel",
    "FoodGroup",
    "FoodGroupModel",
    "FoodModel",
    "Gender",
    "GenderModel",
    "InsertDate",
    "InsertDateModel",
    "InsertUpdateDate",
    "InsertUpdateDateModel",
    "IsValid",
    "IsValidModel",
    "LastUsedPasswords",
    "LastUsedPasswordsModel",
    "Login",
    "LoginAudit",
    "LoginAuditModel",
    "LoginModel",
    "MaritalStatus",
    "MaritalStatusModel",
    "Menu",
    "MenuModel",
    "Name",
    "NameModel",
    "Permission",
    "PermissionModel",
    "Person",
    "PersonModel",
    "PersonType",
    "Resource",
    "ResourceModel",
    "Role",
    "RoleModel",
    "SerialID",
    "SerialIDModel",
    "SimpleTable",
    "SimpleTableModel",
    "State",
    "StateModel",
    "Title",
    "TitleModel",
    "UniqName",
    "UniqNameModel",
    "User",
    "UserContactDocument",
    "UserContactDocumentModel",
    "UserModel",
]
