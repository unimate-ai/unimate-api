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

from src.account.exceptions import (
    UnauthorizedOperationException
)

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

@friends_router.get("/", status_code=HTTPStatus.OK, response_model=GenericAPIResponseModel)
def fetch_my_friends(
    x_current_user: Annotated[EmailStr | None, Header()] = None,
    session: Session = Depends(get_db),
):
    try:
        if x_current_user is None:
            raise UnauthorizedOperationException()
        
        response = FriendsService.fetch_my_friends(
            session=session,
            current_user_email=x_current_user,
        )

        return build_api_response(response)
    except UnauthorizedOperationException as err:
        response = GenericAPIResponseModel(
            status=HTTPStatus.UNAUTHORIZED,
            message="You are not logged in!",
            error="Unauthorized: Failed to perform this operation. Try logging in with the required permissions."
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
