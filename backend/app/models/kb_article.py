import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class KBCategory(str, Enum):
    general = "general"
    billing = "billing"
    technical = "technical"
    account = "account"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class KnowledgeBaseArticle(Base):
    __tablename__ = "knowledge_base_articles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=KBCategory.general.value,
    )
    views: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        default=_utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=_utc_now,
        onupdate=_utc_now,
    )
