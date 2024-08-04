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

class EventSchema(BaseModel):
    name: str = Field(..., max_length=255)
    organizer: str = Field(..., max_length=255)
    is_campus_event: bool
    start_time: datetime
    end_time: datetime
    interests: List[str]
    location: str = Field(..., max_length=255)
    description: str

class EventModelSchema(EventSchema, UniMateBaseSchema):
    pass

class FetchEventPayload(BaseModel):
    id: UUID4