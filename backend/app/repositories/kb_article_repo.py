from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.models.kb_article import KnowledgeBaseArticle
from app.repositories.base_repo import BaseRepository


class KnowledgeBaseArticleRepository(BaseRepository[KnowledgeBaseArticle]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, KnowledgeBaseArticle)

    async def list_filtered(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[KnowledgeBaseArticle], int]:
        query = select(KnowledgeBaseArticle)
        count_query = select(func.count()).select_from(KnowledgeBaseArticle)

        conditions = []
        if category:
            conditions.append(KnowledgeBaseArticle.category == category)
        if search:
            conditions.append(KnowledgeBaseArticle.title.ilike(f"%{search}%"))

        if conditions:
            from sqlalchemy import and_
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        result = await self.db.execute(
            query.order_by(KnowledgeBaseArticle.created_at.desc()).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        return items, total

    async def increment_views(self, article_id: UUID) -> None:
        article = await self.get_by_id(article_id)
        if article:
            article.views += 1
            await self.db.commit()
