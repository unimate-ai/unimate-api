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

class Event(UniMateBaseModel):
    __tablename__ = "events"

    name = Column(String(255))
    organizer = Column(String(255))
    is_campus_event = Column(Boolean())
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    interests = Column(ARRAY(String(255)))
    location = Column(String(255))
    description = Column(String())

