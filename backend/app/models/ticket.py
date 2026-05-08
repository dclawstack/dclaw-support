import uuid
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    waiting = "waiting"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default_factory=uuid.uuid4
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=TicketStatus.open.value,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=TicketPriority.medium.value,
    )
    customer_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        default_factory=_utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        default_factory=_utc_now,
        onupdate=_utc_now,
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="ticket",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
