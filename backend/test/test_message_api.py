import pytest
from uuid import UUID
from sqlalchemy import select
from app.model.session import Session
from app.model.message import Message
from app.schema.message_schema import MessageRead
from app.schema.session_schema import SessionRead

@pytest.mark.asyncio
async def test_send_query_valid_session(db_session, client):
    create_resp = client.post("/addChat")
    assert create_resp.status_code == 200
    session_id = UUID(create_resp.json()["id"])

    request_data = {"query": "Привет", "sessionId": str(session_id)}
    send_resp = client.post("/sendQuery", json=request_data)
    assert send_resp.status_code == 200

    resp_obj = MessageRead.model_validate(send_resp.json())
    assert resp_obj.content == "Привет"
    assert isinstance(resp_obj.id, int)
    assert resp_obj.created_at is not None

    result = await db_session.execute(select(Message).where(Message.id == resp_obj.id))
    message_in_db = result.scalar_one_or_none()
    assert message_in_db is not None
    assert message_in_db.content == resp_obj.content
    assert message_in_db.session_id == resp_obj.session_id

@pytest.mark.asyncio
async def test_send_query_nonexistent_session(client):
    invalid_session_id = UUID("00000000-0000-0000-0000-000000000000")
    request_data = {"query": "Тестовый запрос", "sessionId": str(invalid_session_id)}
    response = client.post("/sendQuery", json=request_data)
    assert response.status_code == 404
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_send_query_deactivated_session(db_session, client):
    create_resp = client.post("/addChat")
    session_id = UUID(create_resp.json()["id"])

    await db_session.execute(
        f"UPDATE session_tab SET is_active = false WHERE id = '{session_id}'"
    )
    await db_session.commit()

    request_data = {"query": "Попытка с деактивированной сессией", "sessionId": str(session_id)}
    response = client.post("/sendQuery", json=request_data)
    assert response.status_code == 404
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_send_query_empty_query(client):
    create_resp = client.post("/addChat")
    session_id = UUID(create_resp.json()["id"])

    request_data = {"query": "", "sessionId": str(session_id)}
    response = client.post("/sendQuery", json=request_data)
    assert response.status_code == 422  # Pydantic validation error

@pytest.mark.asyncio
async def test_send_query_long_query(client):
    create_resp = client.post("/addChat")
    session_id = UUID(create_resp.json()["id"])

    long_text = "a" * 2500
    request_data = {"query": long_text, "sessionId": str(session_id)}
    response = client.post("/sendQuery", json=request_data)
    assert response.status_code == 422  # превышение max_length
