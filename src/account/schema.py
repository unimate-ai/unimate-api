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

class RegisterSchema(BaseModel):
    name: str = Field(..., max_length=255) 
    student_email: EmailStr
    major: str = Field(..., max_length=255)
    cohort_year: int
    graduation_year: int
    interests: List[str]

class RegisterResponseSchema(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime

class UserModelSchema(RegisterSchema, UniMateBaseSchema):
    pass

class SocialsSchema(BaseModel):
    social_type: str = Field(..., max_length=255)
    url: str

class SocialsResponseSchema(SocialsSchema):
    owner_email: EmailStr

class SocialsModelSchema(SocialsSchema, UniMateBaseSchema):
    owner_id: UUID4