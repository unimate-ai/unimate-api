from http import HTTPStatus
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from unimate_logger import logger
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

from src.interest.service import InterestService
from src.interest.schema import InterestSchema

VERSION = "v1"
ENDPOINT = "interest"

interests_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)

@interests_router.post("/")
def create_interest(
    payload: InterestSchema,
    session: Session = Depends(get_db),
):
    try:
        response = InterestService.create_interest(
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