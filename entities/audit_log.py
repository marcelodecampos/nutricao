"""audit log table for application"""

from sqlalchemy import (
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import SerialID, InsertDate


class AuditLog(SerialID, InsertDate):
    """audit data class"""

    __tablename__ = "audit_log"
    target_data: Mapped[JSON] = mapped_column(JSON, nullable=False, sort_order=10)
    action: Mapped[str] = mapped_column(
        String(128),
        index=True,
        nullable=False,
        sort_order=10,
    )
    __table_args__ = {"schema": "audit"}
