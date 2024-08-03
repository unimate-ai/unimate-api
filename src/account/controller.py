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

from src.account.service import AccountService
from src.account.model import User
from src.account.schema import (
    RegisterSchema,
    SocialsSchema,
)
from src.account.exceptions import (
    UserAlreadyExistsException,
    RegistrationFailedException,
    UnauthorizedOperationException,
)


VERSION = "v1"
ENDPOINT = "account"

account_router = APIRouter(
    prefix=f"/{VERSION}/{ENDPOINT}",
    tags=[ENDPOINT]
)

@account_router.post("/register", status_code=HTTPStatus.CREATED, response_model=GenericAPIResponseModel)
def register_user(
    payload: RegisterSchema = Body(),
    session: Session = Depends(get_db),
):
    try:
        response = AccountService.register_user(
            session=session,
            payload=payload,
        )

        return build_api_response(response)
    
    except UserAlreadyExistsException as err:
        response = GenericAPIResponseModel(
            status=HTTPStatus.CONFLICT,
            message=err.__str__(),
            error=err.__str__(),
        )

        return build_api_response(response)
    except RegistrationFailedException as err:
        response = GenericAPIResponseModel(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=err.__str__(),
            error=err.__str__(),
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
    
@account_router.post("/socials")
def create_socials(
    x_current_user: Annotated[EmailStr | None, Header()] = None,
    payload: SocialsSchema = Body(),
    session: Session = Depends(get_db),
):
    try:
        if x_current_user is None:
            raise UnauthorizedOperationException()
        
        response = AccountService.create_user_socials(
            session=session,
            payload=payload,
            x_current_user=x_current_user,
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