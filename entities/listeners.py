#!  python3
# -*- coding: utf-8 -*-
# pylint: disable=not-callable, unused-argument, logging-fstring-interpolation
"""module for listeners events on tables"""

import logging
from datetime import datetime
from sqlalchemy import event
from .person import Person


LOGGER = logging.getLogger(__name__)


@event.listens_for(Person, "before_update", propagate=True)
def person_before_update_listener(mapper, connection, target):
    """before update listener"""
    LOGGER.debug(f"Mapper: {type(mapper)}-{str(mapper)}")
    LOGGER.debug(f"Connection: {type(connection)}-{str(connection)}")
    LOGGER.debug(f"Target: {type(target)}-{str(target)}")
    if isinstance(target, Person):
        target.time_updated = datetime.today()
