#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import logging
from typing import Any
from sqlalchemy import select, inspect
import reflex as rx
from mainsystem.app_state import AppState
from entities import SQLALCHEMY_CLASS_REGISTRY


class SimpleTableState(AppState):
    """State for the simple table component."""

    columns: list[dict] = []
    fields: list[str] = []
    cell_id_width: str = "50px"
    multiple_select: bool = False
    title: str = "Simple Table"
    data: list[list] = []
    index: list[tuple] = []
    selected_items: dict[int, bool] = {}

    _logger = logging.getLogger(__name__)

    @rx.event
    async def handle_create_record(self):
        """Handle the creation of a new record."""
        self._logger.debug("Creating a new record in the simple table.")
        yield rx.toast.info("New record creation is not implemented yet.")

    @rx.event
    async def handle_delete_records(self):
        """Handle the deletion of selected records."""
        self._logger.debug("Deleting selected records in the simple table. {self.selected_items}")
        yield rx.toast.info("All selected records will be deleted.")

    @rx.event
    async def handle_id_select_all(self):
        """Handle the selection of all IDs."""
        self._logger.debug("Selecting all IDs in the simple table.")
        yield rx.toast.info("Select all IDs is not implemented yet.")

    @rx.event
    async def handle_id_select_none(self):
        """Handle the selection of no IDs."""
        self._logger.debug("Selecting no IDs in the simple table.")
        yield rx.toast.info("Select no IDs is not implemented yet.")

    @rx.event
    async def handle_id_select_invert(self):
        """Handle the selection of inverted IDs."""
        self._logger.debug("Selecting inverted IDs in the simple table.")
        yield rx.toast.info("Select inverted IDs is not implemented yet.")

    async def load_data(self, table_definition: dict):
        """Execute a SQL query and return the results."""
        entity = table_definition.get("entity", None)
        if not entity:
            errmsg = f"{entity.__name__} entity is not defined in the table definition."
            raise ValueError(errmsg)
        self._logger.debug(f"loading entity: {entity}")
        with rx.session() as session:
            limit = table_definition.get("limit", 200)
            if limit > 200:
                self._logger.warning(f"Limit {limit} is greater than 200, setting to 200.")
                limit = 200

            entity_class = SQLALCHEMY_CLASS_REGISTRY.get(entity, None)
            query = select(entity_class).limit(limit)
            result = session.scalars(query).fetchall()
            for row in result:
                data = [getattr(row, field, None) for field in self.fields]
                index = inspect(row).identity
                self.data.append(data)
                self.index.append(index)
                self.title = table_definition.get("title", "Simple Table")
            self._logger.debug(f"Data loaded: {self.data}")
            self.selected_items = {}
            session.rollback()  ##always readonly

    @rx.event(background=True)
    async def handle_table_definition(self, table_definition: dict):
        """Handle the setting of the table definition."""
        if not table_definition:
            errmsg = "Table definition cannot be empty."
            self._logger.error(errmsg)
            raise ValueError(errmsg)
        self._logger.debug(
            f"Setting table definition for the simple table. TableDefinition={table_definition}"
        )
        async with self:
            self.columns = table_definition.get("columns", [])
            self.fields = [column["field"] for column in table_definition.get("columns", [])]
            entity = table_definition.get("entity", None)
            self.data = table_definition.get("data", [])
            self.multiple_select = table_definition.get("multiple_select", False)
            if entity:
                self._logger.debug(f"loading entity {entity} data")
                await self.load_data(table_definition)

    @rx.event
    async def handle_checkbox_on_change(self, value: bool, index: int):
        """Handle checkbox change event."""
        self._logger.debug(f"Checkbox changed for index: {index}")
        # Implement logic to handle checkbox change
        if value:
            self.selected_items[index] = value
        else:
            if index in self.selected_items:
                del self.selected_items[index]
        yield rx.toast.info(
            f"Checkbox for index {index} {value} changed. List has {len(self.selected_items)} selected items."
        )

    def get_column_list(self, index: int) -> list[Any]:
        """Get the list of columns for the simple table."""
        if not self.columns:
            self._logger.warning("No columns defined in the simple table.")
            return []
        if index < 0 or index >= len(self.columns):
            errmsg = f"Index {index} is out of bounds for columns list."
            self._logger.error(errmsg)
            raise IndexError(errmsg)
        return self.data[index][1] if self.data and len(self.data) > index else []

    @rx.var
    def is_multiple_select(self) -> bool:
        """Check if the simple table supports multiple selection."""
        return self.multiple_select and len(self.selected_items) > 0


def simple_table_id_column_header_cell() -> rx.Component:
    """Return the ID cell component for the simple table."""
    return rx.table.column_header_cell(
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    "ID",
                    rx.icon("chevrons-down", size=20, stroke_width=1),
                    variant="soft",
                    size="1",
                    spacing="0",
                    padding="0",
                    border="none",
                    width="100%",
                    height="100%",
                    id="simple-table-id-column-header-button",
                ),
            ),
            rx.menu.content(
                rx.menu.item("Todos", on_click=SimpleTableState.handle_id_select_all),
                rx.menu.item("Inverter", on_click=SimpleTableState.handle_id_select_invert),
                rx.menu.item("Nenhum", on_click=SimpleTableState.handle_id_select_none),
            ),
        ),
        width=SimpleTableState.cell_id_width,
        spacing="0",
        padding="0",
        id="simple-table-header-id",
        border="1px solid rgb(100, 100, 100)",
    )


def simple_table_column_header_cell(column_header: dict) -> rx.Component:
    """Return the ID cell component for the simple table."""
    field: str = column_header.get("field", None)
    label: str = column_header.get("label", field)
    cell_width: str = column_header.get("width", "auto")
    return rx.table.column_header_cell(
        rx.button(
            label,
            variant="soft",
            size="1",
            spacing="0",
            padding="0",
            border="none",
            width="100%",
            height="100%",
            id=f"simple-table-column-header-cell-button-{field}",
        ),
        spacing="0",
        padding="0",
        id=f"simple-table-header-cell-{field}",
        border="1px solid rgb(100, 100, 100)",
        width=cell_width,
        align=column_header.get("align", "left"),
    )


def simple_table_row_cell_id(index: int) -> rx.Component:
    """Create a simple table component."""
    return rx.table.cell(
        rx.checkbox(
            id="simple-table-cell-id-checkbox",
            on_change=lambda value: SimpleTableState.handle_checkbox_on_change(value, index),
        ),
        id="simple-table-cell-id",
        border="1px solid rgb(100, 100, 100)",
        width=SimpleTableState.cell_id_width,
    )


def simple_table_row_cell(cell_value, rowindex: int, colindex: int) -> rx.Component:
    """Create a simple table cell component."""
    return rx.table.cell(
        rx.text(cell_value, id=f"simple-table-cell-text-{rowindex}-{colindex}"),
        border="1px solid rgb(100, 100, 100)",
    )


def simple_table_row(index: int) -> rx.Component:
    """Create a simple table component."""
    return rx.table.row(
        simple_table_row_cell_id(index),
        rx.foreach(
            SimpleTableState.data[index],
            lambda record, colindex: simple_table_row_cell(record, index, colindex),
        ),
        id="simple-table-row",
        _hover={"background_color": "rgba(100, 100, 100, 0.2)"},
    )


def simple_table_body() -> rx.Component:
    """Create a simple table component."""
    return rx.table.body(
        rx.foreach(
            SimpleTableState.data,
            lambda row, index: simple_table_row(index),
        ),
        id="simple-table-body",
    )


def simple_table_component(table_definition: dict) -> rx.Component:
    """Create a simple table component."""
    if not table_definition:
        raise ValueError("Table definition cannot be empty.")
    if not table_definition.get("columns"):
        raise ValueError("Columns table definitions cannot be empty.")
    return rx.vstack(
        rx.hstack(
            rx.heading(
                SimpleTableState.title,
                class_id="simple-table-title",
                size="4",
                align="left",
                trim="both",
                width="100%",
                weight="light",
                id="simple-table-heading",
            ),
            rx.button(
                rx.icon("plus", size=20),
                "Novo Registro",
                id="simple-table-new-record-button",
                on_click=SimpleTableState.handle_create_record,
            ),
            rx.button(
                rx.icon("minus", size=20),
                "Excluir os Resgistros Selecionados",
                id="simple-table-delete-records-button",
                on_click=SimpleTableState.handle_create_record,
                style={
                    "visibility": rx.cond(SimpleTableState.is_multiple_select, "visible", "hidden")
                },
            ),
            width="100%",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.cond(SimpleTableState.multiple_select, simple_table_id_column_header_cell()),
                    rx.foreach(
                        SimpleTableState.columns,
                        lambda col: simple_table_column_header_cell(col),
                    ),
                ),
                id="simple-table-header",
            ),
            simple_table_body(),
            width="100%",
            height="400px",
            class_id="simple-table",
            size="1",
            id="simple-table-root",
        ),
        on_mount=lambda: SimpleTableState.handle_table_definition(
            table_definition=table_definition
        ),  # pylnt: disable=no-value-for-parameter
    )


def test_simple_table() -> rx.Component:
    """Test the simple_table function."""
    json_table_definition = {
        "data": [],
        "columns": [
            {
                "field": "formatted_cpf",
                "label": "CPF",
                "width": "150px",
            },
            {
                "field": "name",
                "label": "Nome",
            },
            {
                "field": "formatted_birthdate",
                "label": "Data de Nascimento",
                "width": "80px",
            },
            {
                "field": "age",
                "label": "Idade",
                "width": "40px",
                "type": "number",
                "align": "right",
            },
            {
                "field": "email",
                "label": "Email",
            },
        ],
        "title": "Tabela Muito Simples",
        "width": "100%",
        "height": "auto",
        "multiple_select": True,
        "entity": "Person",
    }
    return simple_table_component(json_table_definition)
