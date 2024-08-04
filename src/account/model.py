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

class User(UniMateBaseModel):
    __tablename__ = "users"

    name = Column(String(255))
    student_email = Column(String(255), unique=True)
    major = Column(String(255))
    cohort_year = Column(Integer())
    graduation_year = Column(Integer())
    interests = Column(ARRAY(String(255)))

class Socials(UniMateBaseModel):
    __tablename__ = "socials"

    owner_id = Column(UUID(), ForeignKey("users.id"))
    social_type = Column(String(255))
    url = Column(String())
