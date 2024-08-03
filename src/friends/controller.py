import uuid
from http import HTTPStatus
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from pydantic import EmailStr

from unimate_logger import logger
from fastapi import (
    APIRouter,
    Request,
    Response,
    Depends,
    Body,
    Header,
)

from fastapi.responses import (
    JSONResponse,
)

from fastapi.encoders import jsonable_encoder

from src.utils.db import get_db
from src.core.schema import GenericAPIResponseModel
from src.utils.response_builder import build_api_response

from src.friends.schema import (
    FriendSchema,
)

from src.friends.service import FriendsService

VERSION = "v1"
ENDPOINT = "friend"

friends_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)

@friends_router.post("/", status_code=HTTPStatus.CREATED, response_model=GenericAPIResponseModel)
def add_friend(
    payload: FriendSchema = Body(),
    session: Session = Depends(get_db),
):
    try:
        response = FriendsService.add_friend(
            session=session,
            payload=payload,
        )

        return build_api_response(response)
    except Exception as err:
        logger.error(err.__str__())
        
        response = GenericAPIResponseModel(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=err.__str__(),
            error=err.__str__(),
        )

        return build_api_response(response)


