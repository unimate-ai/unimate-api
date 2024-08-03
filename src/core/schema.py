from typing import Optional, Any
from datetime import datetime

from pydantic import (
    BaseModel,
    UUID4
)

class GenericAPIResponseModel(BaseModel):
    """Generic Response Model for all API Responses"""
    status: Optional[int]
    message: Optional[str]
    data: Optional[Any] = None
    error: Optional[str] = None
    

class UniMateBaseSchema(BaseModel):
    """
    Base Pydantic schema for UniMate
    """

    id: UUID4
    created_at: datetime
    updated_at: datetime
    is_deleted: bool