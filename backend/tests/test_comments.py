import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_comment(client):
    ticket_payload = {
        "subject": "Comment Ticket",
        "description": "Desc",
        "customer_email": "comment@example.com",
    }
    ticket_resp = await client.post("/api/v1/tickets/", json=ticket_payload)
    ticket_id = ticket_resp.json()["id"]

    comment_payload = {
        "ticket_id": ticket_id,
        "author": "Agent",
        "body": "This is a comment",
        "is_internal": False,
    }
    response = await client.post("/api/v1/comments/", json=comment_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Agent"
    assert data["body"] == "This is a comment"


@pytest.mark.asyncio
async def test_create_comment_ticket_not_found(client):
    comment_payload = {
        "ticket_id": str(uuid4()),
        "author": "Agent",
        "body": "Comment",
    }
    response = await client.post("/api/v1/comments/", json=comment_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_comments(client):
    ticket_payload = {
        "subject": "List Comments Ticket",
        "description": "Desc",
        "customer_email": "listcomments@example.com",
    }
    ticket_resp = await client.post("/api/v1/tickets/", json=ticket_payload)
    ticket_id = ticket_resp.json()["id"]

    comment_payload = {
        "ticket_id": ticket_id,
        "author": "Agent",
        "body": "Comment 1",
    }
    await client.post("/api/v1/comments/", json=comment_payload)

    response = await client.get(f"/api/v1/comments/ticket/{ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_delete_comment(client):
    ticket_payload = {
        "subject": "Delete Comment Ticket",
        "description": "Desc",
        "customer_email": "delcomment@example.com",
    }
    ticket_resp = await client.post("/api/v1/tickets/", json=ticket_payload)
    ticket_id = ticket_resp.json()["id"]

    comment_payload = {
        "ticket_id": ticket_id,
        "author": "Agent",
        "body": "To delete",
    }
    comment_resp = await client.post("/api/v1/comments/", json=comment_payload)
    comment_id = comment_resp.json()["id"]

    response = await client.delete(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 204

    list_resp = await client.get(f"/api/v1/comments/ticket/{ticket_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 0
