import pytest
from app.model.session import Session
from sqlalchemy import select
from uuid import UUID

@pytest.mark.asyncio
async def test_add_chat_and_check_db(db_session, client):
    response = client.post("/addChat")
    assert response.status_code == 200
    data = response.json()
    session_id = UUID(data["id"])

    result = await db_session.execute(select(Session).where(Session.id == session_id))
    session_in_db = result.scalar_one_or_none()

    assert session_in_db is not None
    assert session_in_db.is_active is True

@pytest.mark.asyncio
async def test_clear_chat_and_check_db(db_session, client):
    create_resp = client.post("/addChat")
    session_id = UUID(create_resp.json()["id"])

    clear_resp = client.delete("/clearChat", params={"sessionId": str(session_id)})
    assert clear_resp.status_code == 200

    result = await db_session.execute(select(Session).where(Session.id == session_id))
    session_in_db = result.scalar_one_or_none()

    assert session_in_db is not None
    assert session_in_db.is_active is False


@pytest.mark.asyncio
async def test_clear_chat_nonexistent_session(client):
    invalid_session_id = UUID("00000000-0000-0000-0000-000000000000")
    response = client.delete("/clearChat", params={"sessionId": str(invalid_session_id)})

    assert response.status_code == 404
    assert "detail" in response.json()