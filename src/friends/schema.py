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

class FriendSchema(BaseModel):
    friend_one: UUID4
    friend_two: UUID4

class FriendModelSchema(FriendSchema, UniMateBaseSchema):
    pass