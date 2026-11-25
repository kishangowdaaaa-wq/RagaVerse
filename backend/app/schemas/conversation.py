from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ConversationCreate(BaseModel):
    title: str = Field(default="New Conversation", min_length=1, max_length=200)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20000)


class MessageResponse(BaseModel):
    id: int
    role: MessageRole
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationDetailResponse(ConversationResponse):
    messages: list[MessageResponse] = Field(default_factory=list)


class ChatResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse
