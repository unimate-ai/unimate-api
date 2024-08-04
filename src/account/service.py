import uuid
from http import HTTPStatus
from typing import List

from pydantic import (
    EmailStr, 
    UUID4,
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

    SocialsSchema,
    SocialsResponseSchema,
    SocialsModelSchema,
)
from src.account.exceptions import (
    UserAlreadyExistsException,
    RegistrationFailedException,
    UnauthorizedOperationException,
)
from src.account import messages as AccountMessages

class AccountService:
    # Business Logic
    @classmethod
    def fetch_all_users(
        cls,
        session: Session,
    ) -> GenericAPIResponseModel:
        try:
            users = session.query(User).all()

            data = {
                "users": users,
            }

            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.OK,
                message="Fetched all users",
                data=data_json,
            )

            return response
        except Exception as err:
            raise err
        

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
                user_id=user.id,
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
        except Exception:
            raise RegistrationFailedException()
        
    @classmethod
    def create_user_socials(
        cls,
        session: Session,
        payload: SocialsSchema,
        current_user_email: EmailStr,
    ) -> GenericAPIResponseModel:
        try:
            user: (User | None) = AccountService.get_user_by_email(
                session=session,
                student_email=current_user_email,
            )

            if not user:
                raise UnauthorizedOperationException()

            socials = cls._create_user_socials(
                session=session,
                user=user,
                payload=payload,
            )
            
            data = SocialsResponseSchema(
                social_type=socials.social_type,
                url=socials.url,
                owner_email=user.student_email,
            )

            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message=AccountMessages.CREATED_SOCIALS,
                data=data_json
            )
            
            return response
        except Exception as err:
            raise err
        
    # Utility methods
    @staticmethod
    def get_user_by_id(
        session: Session,
        user_id: UUID4,
    ) -> User | None:
        """
        Fetch a user from the database based on ID
        """

        user = session.query(User) \
                .filter(User.id == user_id, User.is_deleted == False) \
                .first()
        
        return user
        
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
        
    @staticmethod
    def _create_user_socials_schema(
        user: User,
        payload: SocialsSchema,
    ) -> SocialsModelSchema:
        time_now_tz = get_datetime_now_melb()
        
        return SocialsModelSchema(
            id=uuid.uuid4(),
            created_at=time_now_tz,
            updated_at=time_now_tz,
            is_deleted=False,

            owner_id=user.id,
            social_type=payload.social_type,
            url=payload.url,
        )
    
    @classmethod
    def _create_user_socials(
        cls,
        session: Session,
        user: User,
        payload: SocialsSchema,
    ) -> Socials:
        socials_model_schema = cls._create_user_socials_schema(
            user=user, 
            payload=payload,
        )

        socials_obj_db = Socials(**socials_model_schema.model_dump())
        
        try:
            session.add(socials_obj_db)
            session.commit()     
            session.refresh(socials_obj_db)

            return socials_obj_db
        except Exception as err:
            session.rollback()
            raise err