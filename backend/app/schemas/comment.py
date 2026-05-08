import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    author: str
    body: str
    is_internal: bool = False


class CommentCreate(CommentBase):
    ticket_id: uuid.UUID


class CommentRead(CommentBase):
    id: uuid.UUID
    ticket_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
