import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

try:
    from entities import Login
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from entities import Login

# an Engine, which the Session will use for connection
# resources
engine = create_engine(
    "postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=menu_test"
)

# create session and add objects
with Session(engine) as session:
    entitites = (Login(user_id=1, password="137375"),)
    session.add_all(entitites)
    session.commit()
