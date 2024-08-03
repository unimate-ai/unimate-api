import uuid
from uuid import UUID
from pytz import timezone
from datetime import datetime

from src.utils.db import Base
from sqlalchemy import (
    Boolean,
    Integer,
    Column,
    UUID,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    TIMESTAMP,
    ARRAY
)
from sqlalchemy.orm import (
    Session,
    relationship
)

from src.core.model import UniMateBaseModel

class Chatroom(UniMateBaseModel):
    __tablename__ = "chatrooms"

    user_one_id = Column(UUID(), ForeignKey("users.id"))
    user_two_id = Column(UUID(), ForeignKey("users.id"))


class ChatMessage(UniMateBaseModel):
    __tablename__ = "chat_messages"
    
    chatroom_id = Column(UUID(), ForeignKey("chatrooms.id"))
    sender_id = Column(UUID(), ForeignKey("users.id"))
    message = Column(String())