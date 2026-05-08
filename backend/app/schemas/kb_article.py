import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class KnowledgeBaseArticleBase(BaseModel):
    title: str
    content: str
    category: str = "general"


class KnowledgeBaseArticleCreate(KnowledgeBaseArticleBase):
    pass


class KnowledgeBaseArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class KnowledgeBaseArticleRead(KnowledgeBaseArticleBase):
    id: uuid.UUID
    views: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KnowledgeBaseArticleList(BaseModel):
    items: list[KnowledgeBaseArticleRead]
    total: int
