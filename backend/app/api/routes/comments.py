from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.comment_repo import CommentRepository
from app.repositories.ticket_repo import TicketRepository
from app.schemas.comment import CommentCreate, CommentRead
from app.models.comment import Comment

router = APIRouter()


@router.get("/ticket/{ticket_id}", response_model=list[CommentRead])
async def list_comments(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = CommentRepository(db)
    items, _ = await repo.list_by_ticket(ticket_id)
    return items


@router.post("/", response_model=CommentRead, status_code=201)
async def create_comment(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    ticket_repo = TicketRepository(db)
    ticket = await ticket_repo.get_by_id(data.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    repo = CommentRepository(db)
    comment = Comment(**data.model_dump())
    created = await repo.create(comment)
    return created


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = CommentRepository(db)
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await repo.delete(comment)
    return None
