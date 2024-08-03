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

class Friend(UniMateBaseModel):
    __tablename__ = "friends"

    friend_one = Column(UUID(), ForeignKey("users.id"))
    friend_two = Column(UUID(), ForeignKey("users.id"))