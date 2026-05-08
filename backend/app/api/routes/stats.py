from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.kb_article import KnowledgeBaseArticle

router = APIRouter()


@router.get("/")
async def get_stats(db: AsyncSession = Depends(get_db)):
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=None)

    open_result = await db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.status == "open")
    )
    open_count = open_result.scalar() or 0

    resolved_today_result = await db.execute(
        select(func.count()).select_from(Ticket).where(
            Ticket.status == "resolved",
            Ticket.updated_at >= today_start,
        )
    )
    resolved_today_count = resolved_today_result.scalar() or 0

    articles_result = await db.execute(
        select(func.count()).select_from(KnowledgeBaseArticle)
    )
    articles_count = articles_result.scalar() or 0

    return {
        "open_tickets": open_count,
        "resolved_today": resolved_today_count,
        "kb_articles": articles_count,
    }
