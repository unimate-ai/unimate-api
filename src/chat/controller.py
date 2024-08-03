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

from src.chat.service import ChatService
from src.chat.schema import (
    ChatroomRequestSchema,
    ChatroomSchema,
    ChatroomModelSchema,
    ChatMessageSchema,
    ChatMessageModelSchema,
)

VERSION = "v1"
ENDPOINT = "chat"

chat_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)

@chat_router.post("/", status_code=HTTPStatus.CREATED, response_model=GenericAPIResponseModel)
def create_chatroom(
    payload: ChatroomRequestSchema,
    x_current_user: Annotated[EmailStr | None, Header()] = None,
    session: Session = Depends(get_db),
):
    try:
        response = ChatService.create_chatroom(
            payload=payload,
            current_user_email=x_current_user,
            session=session,
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
    
@chat_router.get("/{chatroom_id}", status_code=HTTPStatus.OK, response_model=GenericAPIResponseModel)
def fetch_chatroom(
    chatroom_id: str,
    x_current_user: Annotated[EmailStr | None, Header()] = None,
    session: Session = Depends(get_db),
):
    try:
        chatroom_uuid = uuid.UUID(chatroom_id)

        response = ChatService.fetch_chatroom(
            current_user_email=x_current_user,
            chatroom_id=chatroom_uuid,
            session=session,
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