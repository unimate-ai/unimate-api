import uuid
from http import HTTPStatus

from pydantic import (
    EmailStr
)

from unimate_logger import logger
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from src.core.schema import GenericAPIResponseModel
from src.utils.time import get_datetime_now_melb

from src.interest.schema import (
    InterestSchema,
    InterestModelSchema,
)
from src.interest.model import Interest
import src.interest.messages as InterestMessages
from src.interest.exceptions import (
    InterestAlreadyExistsException,
)

class InterestService:
    @classmethod
    def create_interest(
        cls,
        session: Session,
        payload: InterestSchema,
    ) -> GenericAPIResponseModel:
        try:
            interest_exists = cls.is_interest_exists(name=payload.name, session=session)
            if interest_exists:
                raise InterestAlreadyExistsException()
            interest = cls._create_interest(
                session=session,
                payload=payload
            )

            data = InterestSchema(
                name=interest.name,
                is_academic=interest.is_academic,
            )

            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message=InterestMessages.CREATED_INTEREST,
                data=data_json,
            )

            return response
        except InterestAlreadyExistsException as err:
            raise err
        except Exception as err:
            raise err

    # Utility methods
    @classmethod
    def is_interest_exists(
        cls,
        name: str,
        session: Session,
    ) -> bool:
        interest = session.query(Interest) \
                    .filter(Interest.name == name) \
                    .first()
        
        if interest is None:
            return False

        return True


    @staticmethod
    def _create_interest_schema(
        payload: InterestSchema,
    ) -> InterestModelSchema:
        return InterestModelSchema(
            id=uuid.uuid4(),
            name=payload.name,
            is_academic=payload.is_academic,
        )

    @classmethod
    def _create_interest(
        cls,
        session: Session,
        payload: InterestSchema,
    ) -> Interest:
        interest_model_schema =  cls._create_interest_schema(payload=payload)
        
        interest_obj_db = Interest(**interest_model_schema.model_dump())

        try:
            session.add(interest_obj_db)
            session.commit()
            session.refresh(interest_obj_db)

            return interest_obj_db
        except Exception as err:
            session.rollback()
            raise err