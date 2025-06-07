#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, logging-fstring-interpolation, disable=unnecessary-lambda, disable=no-value-for-parameter
"""init file for utils module."""

import logging
from typing import Any

import reflex as rx

from mainsystem.app_state import AppState


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
        count = [key for key, value in self.selected_items.items() if value is True]
        itens_to_delete = [self.data[index][1] for index in count]
        self._logger.debug(
            f"Deleting selected records in the simple table. {itens_to_delete}"
        )
        yield rx.toast.info("All selected records will be deleted.")

    @rx.event
    async def handle_id_select_all(self):
        """Handle the selection of all IDs."""
        self._logger.debug("Selecting all IDs in the simple table.")
        self.selected_items = {index: True for index, item in enumerate(self.data)}
        self._logger.debug(f"{self.selected_items}")

    @rx.event
    async def handle_id_select_none(self):
        """Handle the selection of no IDs."""
        self._logger.debug("Selecting no IDs in the simple table.")
        self.selected_items = {}
        self._logger.debug(f"{self.selected_items}")

    @rx.event
    async def handle_id_select_invert(self):
        """Handle the selection of inverted IDs."""
        self._logger.debug("Selecting inverted IDs in the simple table.")
        yield rx.toast.info("Select inverted IDs is not implemented yet.")

    @rx.event
    async def on_delete_selected_records(self):
        """Handle the deletion of selected records."""
        self._logger.debug("Deleting selected records in the simple table.")
        yield rx.toast.warning("Delete selected records is not implemented yet.")

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
            (
                f"Checkbox for index {index} {value} changed. "
                f"List has {len(self.selected_items)} selected items."
            )
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
        count = [item for item in self.selected_items.values() if item is True]
        return len(count) > 1
