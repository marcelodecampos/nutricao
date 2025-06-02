#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=(not-callable, inherit-non-class, no-name-in-module)
#
"""test module"""

import sys
import os
from faker import Faker

# just in case
sys.path.append(os.getcwd())


FILE = "/mnt/c/temp/grupos.csv"


with open(FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()
lines = [line.strip() for line in lines if line.strip()]

with (
    open("/mnt/c/temp/male.txt", "w", encoding="utf-8") as male_file,
    open("/mnt/c/temp/female.txt", "w", encoding="utf-8") as female_file,
):
    for line in lines:
        itens = line.split(",")
        if len(itens) < 2:
            continue
        name = f"'{itens[0].strip().capitalize()}',"
        if itens[1].strip().startswith("M"):
            male_file.write("\t" + "\t" + name + "\n")
        else:
            female_file.write("\t" + "\t" + name + "\n")
