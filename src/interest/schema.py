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

class InterestSchema(BaseModel):
    name: str = Field(..., max_length=255)
    is_academic: bool

class InterestModelSchema(InterestSchema):
    id: UUID4