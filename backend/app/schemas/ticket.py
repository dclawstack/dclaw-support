import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.schemas.comment import CommentRead


class TicketBase(BaseModel):
    subject: str
    description: str
    status: str = "open"
    priority: str = "medium"
    customer_email: str
    customer_name: Optional[str] = None
    assigned_to: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    assigned_to: Optional[str] = None


class TicketRead(TicketBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    comments: List[CommentRead] = []

    model_config = ConfigDict(from_attributes=True)


class TicketList(BaseModel):
    items: List[TicketRead]
    total: int
