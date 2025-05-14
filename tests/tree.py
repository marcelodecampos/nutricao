# python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods, missing-function-docstring
"""init module for login component."""

import pickle
from time import time
import psycopg
from treelib import Tree


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        return result

    return wrap_func


@timer_func
def load_menu(session) -> Tree:
    """get all menus from database without parent"""
    menu_tree: Tree = Tree()

    with session.cursor() as cursor:
        menu_tree.create_node("Root", "root")
        cursor.execute("SELECT * FROM vw_menu")
        for row in cursor:
            menu_tree.create_node(row[1], row[0], row[5] or "root", row)
    return menu_tree


@timer_func
def serialize(tree: Tree):
    with open("tree.pkl", "wb") as f:
        pickle.dump(tree, f)


@timer_func
def run():
    print("Running")
    url = "dbname=minhanutri user=postgres host=db.local"
    print("Connecting")
    conn = psycopg.connect(url)
    print("Connected")
    main_tree = load_menu(conn)
    main_tree.show()
    serialize(main_tree)
    conn.close()


if __name__ == "__main__":
    run()
