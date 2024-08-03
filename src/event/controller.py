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

from src.event.schema import (
    EventSchema,
)
from src.event.service import EventService

VERSION = "v1"
ENDPOINT = "event"

event_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)

@event_router.post("/", status_code=HTTPStatus.CREATED, response_model=GenericAPIResponseModel)
def create_event(
    payload: EventSchema = Body(),
    session: Session = Depends(get_db),
):
    try:
        response = EventService.create_event(
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
    
@event_router.get("/", status_code=HTTPStatus.OK, response_model=GenericAPIResponseModel)
def fetch_all_events(
    session: Session = Depends(get_db),
): 
    try: 
        response = EventService.fetch_all_events(
            session=session
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
    
@event_router.get("/{event_id}", status_code=HTTPStatus.OK, response_model=GenericAPIResponseModel)
def fetch_event_by_id(
    event_id: str,
    session: Session = Depends(get_db),
):
    try:
        event_uuid = uuid.UUID(event_id)

        response = EventService.fetch_event_details(
            payload=event_uuid,
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