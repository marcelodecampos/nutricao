#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module)
#
"""test module"""

import email
import sys
import os
from faker import Faker
from typeguard import value

# just in case
sys.path.append(os.getcwd())


fake = Faker("pt_BR")
emails_dict = {}
nome_dict = []
for index in range(200000):
    email = fake.email(False)
    if email not in emails_dict:
        emails_dict[email] = fake.name()
    if index and index % 500 == 0:
        print(f"Gerados {index} emails")
print(f"Total de emails gerados: {len(emails_dict)}")
