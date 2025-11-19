from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.depends import database, session_repo, message_repo, faq_repo
from app.core.exception.session_exception import SessionNotFound
from app.core.exception.message_exception import MessageNotFound
from app.core.exception.faq_exception import FAQNotFound
from app.schema.sessionSchema import SessionRead
from app.schema.messageSchema import MessageCreate, MessageRead
from app.schema.faqSchema import FAQRead

router = APIRouter()

# TODO: Нужны JWT токены

@router.post("/addChat", response_model=SessionRead)
async def add_chat():
    async with database.session() as session:
        new_session = await session_repo.create_session(session=session)
    return new_session

@router.post("/sendQuery", response_model=MessageRead)
async def send_query(query: str, sessionId: UUID):
    async with database.session() as session:
        message_dto = MessageCreate(session_id=sessionId, content=query)
        # TODO: добавить осмысленный ответ
        new_message = await message_repo.create_message(session=session, message=message_dto)
    return new_message

@router.delete("/clearChat")
async def clear_chat(sessionId: UUID):
    try:
        async with database.session() as session:
            updated_session = await session_repo.deactivate_session(session=session, session_id=sessionId)
    except SessionNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {"status": "cleared"}

@router.get("/getFAQ", response_model=list[FAQRead])
async def get_all_faq():
    async with database.session() as session:
        all_faq = await faq_repo.get_all_faq(session=session)
    return all_faq

@router.get("/getFAQ/{id}", response_model=FAQRead)
async def get_faq_by_id(id: int):
    try:
        async with database.session() as session:
            faq_item = await faq_repo.get_by_id(session=session, faq_id=id)
    except FAQNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return faq_item
