from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.kb_article_repo import KnowledgeBaseArticleRepository
from app.schemas.kb_article import (
    KnowledgeBaseArticleCreate,
    KnowledgeBaseArticleUpdate,
    KnowledgeBaseArticleRead,
    KnowledgeBaseArticleList,
)
from app.models.kb_article import KnowledgeBaseArticle

router = APIRouter()


@router.get("/", response_model=KnowledgeBaseArticleList)
async def list_articles(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = KnowledgeBaseArticleRepository(db)
    items, total = await repo.list_filtered(category, search, limit, offset)
    return KnowledgeBaseArticleList(items=items, total=total)


@router.post("/", response_model=KnowledgeBaseArticleRead, status_code=201)
async def create_article(
    data: KnowledgeBaseArticleCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = KnowledgeBaseArticleRepository(db)
    article = KnowledgeBaseArticle(**data.model_dump())
    created = await repo.create(article)
    return created


@router.get("/{article_id}", response_model=KnowledgeBaseArticleRead)
async def get_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = KnowledgeBaseArticleRepository(db)
    article = await repo.get_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await repo.increment_views(article_id)
    await db.refresh(article)
    return article


@router.patch("/{article_id}", response_model=KnowledgeBaseArticleRead)
async def update_article(
    article_id: UUID,
    data: KnowledgeBaseArticleUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = KnowledgeBaseArticleRepository(db)
    article = await repo.get_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(article, field, value)
    await db.commit()
    await db.refresh(article)
    return article


@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = KnowledgeBaseArticleRepository(db)
    article = await repo.get_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await repo.delete(article)
    return None
