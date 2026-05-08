import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_ticket(client):
    payload = {
        "subject": "Test Ticket",
        "description": "This is a test ticket",
        "status": "open",
        "priority": "high",
        "customer_email": "test@example.com",
        "customer_name": "Test User",
    }
    response = await client.post("/api/v1/tickets/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["subject"] == "Test Ticket"
    assert data["priority"] == "high"
    assert data["customer_email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_tickets(client):
    payload = {
        "subject": "List Ticket",
        "description": "Desc",
        "customer_email": "list@example.com",
    }
    await client.post("/api/v1/tickets/", json=payload)
    response = await client.get("/api/v1/tickets/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_get_ticket(client):
    payload = {
        "subject": "Get Ticket",
        "description": "Desc",
        "customer_email": "get@example.com",
    }
    create_resp = await client.post("/api/v1/tickets/", json=payload)
    ticket_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Get Ticket"


@pytest.mark.asyncio
async def test_get_ticket_not_found(client):
    response = await client.get(f"/api/v1/tickets/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_ticket(client):
    payload = {
        "subject": "Update Ticket",
        "description": "Desc",
        "customer_email": "update@example.com",
    }
    create_resp = await client.post("/api/v1/tickets/", json=payload)
    ticket_id = create_resp.json()["id"]

    update_payload = {"status": "resolved", "assigned_to": "agent1"}
    response = await client.patch(f"/api/v1/tickets/{ticket_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "resolved"
    assert data["assigned_to"] == "agent1"


@pytest.mark.asyncio
async def test_delete_ticket(client):
    payload = {
        "subject": "Delete Ticket",
        "description": "Desc",
        "customer_email": "delete@example.com",
    }
    create_resp = await client.post("/api/v1/tickets/", json=payload)
    ticket_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/tickets/{ticket_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_tickets_by_status(client):
    payload = {
        "subject": "Open Ticket",
        "description": "Desc",
        "status": "open",
        "customer_email": "filter@example.com",
    }
    await client.post("/api/v1/tickets/", json=payload)

    response = await client.get("/api/v1/tickets/?status=open")
    assert response.status_code == 200
    data = response.json()
    assert all(t["status"] == "open" for t in data["items"])


@pytest.mark.asyncio
async def test_filter_tickets_by_priority(client):
    payload = {
        "subject": "Urgent Ticket",
        "description": "Desc",
        "priority": "urgent",
        "customer_email": "urgent@example.com",
    }
    await client.post("/api/v1/tickets/", json=payload)

    response = await client.get("/api/v1/tickets/?priority=urgent")
    assert response.status_code == 200
    data = response.json()
    assert all(t["priority"] == "urgent" for t in data["items"])


@pytest.mark.asyncio
async def test_search_tickets(client):
    payload = {
        "subject": "Searchable Subject",
        "description": "Desc",
        "customer_email": "search@example.com",
    }
    await client.post("/api/v1/tickets/", json=payload)

    response = await client.get("/api/v1/tickets/?search=Searchable")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
