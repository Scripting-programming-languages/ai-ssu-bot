from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    content: str = Field(..., max_length=2000)

class MessageCreate(MessageBase):
    session_id: UUID

class MessageRead(MessageBase):
    id: int
    session_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
