#!  python3
# -*- coding: utf-8 -*-
"""Entity modules"""

from .base import Base, SerialID, InsertUpdateDate, Name, UniqName, SimpleTable
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
from .login import Login


__all__ = [
    "Base",
    "SerialID",
    "InsertUpdateDate",
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
]

__version__ = "0.0.1"
