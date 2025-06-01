import os, sys
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

try:
    from entities import Person
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from entities import Person


# an Engine, which the Session will use for connection
# resources
def get_session():
    """get session for test purposes"""

    url = "postgresql+psycopg://postgres:curiosidade@db.local:5432/minhanutri?application_name=menu_test"
    engine = create_engine(url)
    session = Session(engine)
    return session


from pprint import pprint


session = get_session()
query = select(Person).where(Person.id == 1)
stmt = session.execute(query)
person = stmt.scalar_one_or_none()
print(dir(person))
pprint(person.__dict__)
pprint(person.__getattribute__)
pprint(getattr(person, "formatted_birthdate"))
