import pytest


@pytest.mark.asyncio
async def test_stats(client):
    response = await client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "open_tickets" in data
    assert "resolved_today" in data
    assert "kb_articles" in data
