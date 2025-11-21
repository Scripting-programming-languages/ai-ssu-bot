import pytest
from sqlalchemy import select
from app.model.faq import FAQ
from app.schema.faq_schema import FAQRead

@pytest.mark.asyncio
async def test_get_all_faq(db_session, client):
    await db_session.execute(
        FAQ.__table__.insert(),
        [
            {"question": "Вопрос 1", "answer": "Ответ 1"},
            {"question": "Вопрос 2", "answer": "Ответ 2"}
        ]
    )
    await db_session.commit()

    response = client.get("/getFAQ")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(item["question"] == "Вопрос 1" for item in data)
    assert any(item["question"] == "Вопрос 2" for item in data)

@pytest.mark.asyncio
async def test_get_faq_by_id_valid(db_session, client):
    faq = FAQ(question="Вопрос тест", answer="Ответ тест")
    db_session.add(faq)
    await db_session.commit()
    await db_session.refresh(faq)

    response = client.get(f"/getFAQ/{faq.id}")
    assert response.status_code == 200

    faq_obj = FAQRead.model_validate(response.json())
    assert faq_obj.id == faq.id
    assert faq_obj.question == "Вопрос тест"
    assert faq_obj.answer == "Ответ тест"

@pytest.mark.asyncio
async def test_get_faq_by_id_nonexistent(client):
    response = client.get("/getFAQ/999999")
    assert response.status_code == 404
    assert "detail" in response.json()
