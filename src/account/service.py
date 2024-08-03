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

from src.account.model import (
    User,
    Socials,
)
from src.account.schema import (
    RegisterSchema,
    UserModelSchema,
    RegisterResponseSchema,
)
from src.account.exceptions import (
    UserAlreadyExistsException,
    RegistrationFailedException,
)
from src.account import messages as AccountMessages

class AccountService:
    @classmethod
    def register_user(
        cls,
        session: Session,
        payload: RegisterSchema,
    ) -> GenericAPIResponseModel:
        user = cls.get_user_by_email(
            session=session, 
            student_email=payload.student_email,
        )

        if user:
            raise UserAlreadyExistsException(user_email=user.student_email)
        
        try:
            user = cls._create_unimate_user(
                session=session,
                payload=payload,
            )

            data = RegisterResponseSchema(
                name=user.name,
                email=user.student_email,
                created_at=user.created_at,
            )
            
            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message=AccountMessages.CREATE_NEW_USER_SUCCESS,
                data=data_json,
            )

            return response
        except Exception as err:
            raise RegistrationFailedException()


    # Utility methods
    @staticmethod
    def get_user_by_email(
        session: Session,
        student_email: EmailStr
    ) -> User | None:
        """
        Fetch a user from User database based on email
        """
        user = session.query(User) \
                .filter(User.student_email == student_email, User.is_deleted == False) \
                .first()
        
        return user
    
    @staticmethod
    def _create_unimate_user_schema(
        payload: RegisterSchema,
    ) -> UserModelSchema:
        time_now_tz = get_datetime_now_melb()

        return UserModelSchema(
            id=uuid.uuid4(),
            created_at=time_now_tz,
            updated_at=time_now_tz,
            is_deleted=False,

            name=payload.name,
            student_email=payload.student_email,
            major=payload.major,
            cohort_year=payload.cohort_year,
            graduation_year=payload.graduation_year,
            interests=payload.interests,
        )
    
    @classmethod
    def _create_unimate_user(
        cls,
        session: Session,
        payload: RegisterSchema,
    ) -> User:
        user_model_schema = cls._create_unimate_user_schema(payload=payload)

        user_obj_db = User(**user_model_schema.model_dump())

        try:
            session.add(user_obj_db)
            session.commit()
            session.refresh(user_obj_db)

            return user_obj_db
        except Exception as err:
            session.rollback()
            raise RegistrationFailedException(err.__str__())