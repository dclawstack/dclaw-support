import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_article(client):
    payload = {
        "title": "Test Article",
        "content": "This is a test article",
        "category": "technical",
    }
    response = await client.post("/api/v1/articles/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["category"] == "technical"
    assert data["views"] == 0


@pytest.mark.asyncio
async def test_list_articles(client):
    payload = {
        "title": "List Article",
        "content": "Content",
        "category": "general",
    }
    await client.post("/api/v1/articles/", json=payload)
    response = await client.get("/api/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_get_article(client):
    payload = {
        "title": "Get Article",
        "content": "Content",
        "category": "billing",
    }
    create_resp = await client.post("/api/v1/articles/", json=payload)
    article_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Article"
    assert data["views"] == 1  # incremented on get


@pytest.mark.asyncio
async def test_get_article_not_found(client):
    response = await client.get(f"/api/v1/articles/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_article(client):
    payload = {
        "title": "Update Article",
        "content": "Content",
        "category": "account",
    }
    create_resp = await client.post("/api/v1/articles/", json=payload)
    article_id = create_resp.json()["id"]

    update_payload = {"title": "Updated Title"}
    response = await client.patch(f"/api/v1/articles/{article_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_article(client):
    payload = {
        "title": "Delete Article",
        "content": "Content",
        "category": "general",
    }
    create_resp = await client.post("/api/v1/articles/", json=payload)
    article_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/articles/{article_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/articles/{article_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_articles_by_category(client):
    payload = {
        "title": "Billing Article",
        "content": "Content",
        "category": "billing",
    }
    await client.post("/api/v1/articles/", json=payload)

    response = await client.get("/api/v1/articles/?category=billing")
    assert response.status_code == 200
    data = response.json()
    assert all(a["category"] == "billing" for a in data["items"])


@pytest.mark.asyncio
async def test_search_articles(client):
    payload = {
        "title": "Searchable Article Title",
        "content": "Content",
        "category": "general",
    }
    await client.post("/api/v1/articles/", json=payload)

    response = await client.get("/api/v1/articles/?search=Searchable")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
