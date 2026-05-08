from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.comment import Comment
from app.repositories.base_repo import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Comment)

    async def list_by_ticket(self, ticket_id: UUID, limit: int = 100, offset: int = 0) -> tuple[list[Comment], int]:
        query = select(Comment).where(Comment.ticket_id == ticket_id)
        count_query = select(func.count()).select_from(Comment).where(Comment.ticket_id == ticket_id)

        result = await self.db.execute(
            query.order_by(Comment.created_at.asc()).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        return items, total
