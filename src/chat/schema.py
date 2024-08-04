from datetime import datetime
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import (
    UUID4,
    BaseModel,
    EmailStr,
    Field,
)

from src.core.schema import (
    UniMateBaseSchema
)

# Client-facing use
class ChatroomRequestSchema(BaseModel):
    friend_id: UUID4

# Internal use
class ChatroomSchema(BaseModel):
    user_one_id: UUID4
    user_two_id: UUID4

class ChatroomModelSchema(ChatroomSchema, UniMateBaseSchema):
    pass

class ChatroomID(BaseModel):
    chatroom_id: UUID4

class ChatroomByEmail(BaseModel):
    user_one_email: EmailStr
    user_two_email: EmailStr

class ChatMessageRequestSchema(BaseModel):
    chatroom_id: UUID4
    message: str

class ChatMessageSchema(BaseModel):
    chatroom_id: UUID4
    sender_id: UUID4
    message: str

class ChatMessageModelSchema(ChatMessageSchema, UniMateBaseSchema):
    pass
