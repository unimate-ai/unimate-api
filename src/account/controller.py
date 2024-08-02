from http import HTTPStatus
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Request,
    Response,
    Depends,
    Body,
)

from fastapi.responses import (
    JSONResponse,
)

from fastapi.encoders import jsonable_encoder

from src.utils.db import get_db
from src.core.schema import GenericAPIResponseModel
from src.utils.response_builder import build_api_response
from src.account.model import User


VERSION = "v1"
ENDPOINT = "account"

account_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)