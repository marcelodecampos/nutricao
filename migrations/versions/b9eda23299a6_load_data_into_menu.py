"""Load data into menu

Revision ID: b9eda23299a6
Revises: 55d2ecc169e5
Create Date: 2025-05-08 01:28:41.167628

"""

from typing import Sequence, Union
from sqlalchemy.orm import Session
from alembic import op
from entities import Menu


# revision identifiers, used by Alembic.
revision: str = "b9eda23299a6"
down_revision: Union[str, None] = "55d2ecc169e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    session: Session = Session(bind=op.get_bind())
    mnu_tabela = Menu(name="Tabelas do Sistema", index=0)
    session.add(mnu_tabela)

    menu_pessoa = Menu(name="Tabelas de Pessoa", index=1, parent=mnu_tabela, icon="person-standing")
    session.add(menu_pessoa)
    session.add(
        Menu(
            name="Escolaridade",
            index=1,
            parent=menu_pessoa,
            url="/system/tables/person/education",
            icon="school",
        )
    )
    session.add(
        Menu(
            name="Gênero",
            index=2,
            parent=menu_pessoa,
            url="/system/tables/person/gender",
            icon="venus-and-mars",
        )
    )
    session.add(
        Menu(
            name="Estado Civil",
            index=3,
            parent=menu_pessoa,
            url="/system/tables/person/marital_status",
        )
    )
    session.add(
        Menu(
            name="Pronome de Tratamento",
            index=4,
            parent=menu_pessoa,
            url="/system/tables/person/title",
        )
    )
    session.add(
        Menu(
            name="Tipo de Documento",
            index=5,
            parent=menu_pessoa,
            url="/system/tables/person/document",
            icon="id-card",
        )
    )
    session.add(
        Menu(
            name="Meio de Contato",
            index=6,
            parent=menu_pessoa,
            url="/system/tables/person/contact",
            icon="mail-question",
        )
    )

    menu_localidade = Menu(name="Tabela de Localidade", index=2, parent=mnu_tabela)
    session.add(menu_localidade)
    session.add(
        Menu(
            name="País",
            index=1,
            parent=menu_localidade,
            url="/system/tables/locality/country",
        )
    )
    session.add(
        Menu(
            name="Estado",
            index=2,
            parent=menu_localidade,
            url="/system/tables/locality/state",
        )
    )
    session.add(
        Menu(
            name="Cidade",
            index=3,
            parent=menu_localidade,
            url="/system/tables/locality/city",
            icon="building-2",
        )
    )

    menu_nutricao = Menu(name="Tabela de Nutrição", index=3, parent=mnu_tabela)
    session.add(menu_nutricao)
    session.add(
        Menu(
            name="Alimentos", index=1, parent=menu_nutricao, url="/system/tables/food", icon="apple"
        )
    )
    session.add(
        Menu(
            name="Componentes",
            index=2,
            parent=menu_nutricao,
            url="/system/tables/food/component",
            icon="soup",
        )
    )
    session.add(
        Menu(
            name="Composição",
            index=3,
            parent=menu_nutricao,
            url="/system/tables/food/composition",
            icon="microwave",
        )
    )
    session.add(
        Menu(
            name="Grupo",
            index=4,
            parent=menu_nutricao,
            url="/system/tables/food/group",
        )
    )

    menu_person = Menu(name="Cadastro de Pessoa", index=4, parent=mnu_tabela)
    session.add(menu_person)
    session.add(Menu(name="Física", index=1, parent=menu_person, url="/user/person", icon="user"))
    session.add(
        Menu(name="Empresa", index=2, parent=menu_person, url="/user/company", icon="factory")
    )
    session.add(
        Menu(name="Login", index=3, parent=menu_person, url="/user/login", icon="key-round")
    )
    session.commit()

    query = """
        create or replace view vw_menu as (
        WITH RECURSIVE menu_hierarchy as (
            select
                id, name, url, icon, parent_id, 1 as level, index
            from
                menu
            where
                is_valid is true and parent_id is null
            union all
            select
                menu.id, menu.name, menu.url, menu.icon, menu.parent_id, mh.level+1 as level, menu.index
            from
                menu inner join menu_hierarchy mh on mh.id = menu.parent_id
            where
                menu.is_valid is true
        )
        select
            id, name, url, icon, parent_id, level, index
        from menu_hierarchy
        order by id
        )"""
    op.execute(query)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE menu RESTART IDENTITY;")
    op.execute("DROP VIEW IF EXISTS vw_menu")
