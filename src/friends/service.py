import uuid
from typing import List
from http import HTTPStatus

from pydantic import (
    EmailStr
)

from unimate_logger import logger
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from src.core.schema import GenericAPIResponseModel
from src.utils.time import get_datetime_now_melb

from src.friends.schema import (
    FriendSchema,
    FriendModelSchema,
)

from src.account.model import User
from src.account.exceptions import (
    UnauthorizedOperationException,
)

from src.friends.model import (
    Friend,
)
from src.friends.exceptions import (
    UserDoesNotExistsException
)
from src.friends import messages as FriendsMessages

from src.account.service import AccountService

class FriendsService:
    # Business Logic
    @classmethod
    def add_friend(
        cls,
        session: Session,
        payload: FriendSchema,
    ) -> GenericAPIResponseModel:
        try:
            # Check if both user exists on database
            user_one = AccountService.get_user_by_id(
                session=session,
                user_id=payload.friend_one,
            )

            if user_one is None:
                raise UserDoesNotExistsException()

            user_two = AccountService.get_user_by_id(
                session=session,
                user_id=payload.friend_one,
            )
            
            if user_two is None:
                raise UserDoesNotExistsException()
            
            # Both user exists at this point, so we add to the Friends table
            friend_conn = cls._create_friends_connection(
                session=session,
                payload=payload,
            )

            data = {
                "friend_one": friend_conn.friend_one,
                "friend_two": friend_conn.friend_two,
            }

            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message=FriendsMessages.FRIENDS_CREATED,
                data=data_json,
            )

            return response
        except Exception as err:
            raise err
        
    @classmethod
    def fetch_my_friends(
        cls,
        session: Session,
        current_user_email: EmailStr,
    ) -> GenericAPIResponseModel:
        user = AccountService.get_user_by_email(
            session=session,
            student_email=current_user_email,
        )

        if user is None:
            raise UserDoesNotExistsException()

        friends_pair_raw = session.query(Friend) \
                        .filter(
                            # OR conditional filtering
                            (Friend.friend_one == user.id) | (Friend.friend_two == user.id)
                        ) \
                        .all()
        
        # Convert List[Friend] into List[User]
        my_friends: List[User] = []

        for pair in friends_pair_raw:
            friend_id = pair.friend_two if pair.friend_one == user.id else pair.friend_one

            friend_user_obj = AccountService.get_user_by_id(
                session=session,
                user_id=friend_id,
            )

            my_friends.append(friend_user_obj)
        
        data = {
            "friends": my_friends,
        }
        
        data_json = jsonable_encoder(data)

        response = GenericAPIResponseModel(
            status=HTTPStatus.OK,
            message="Successfully fetched all friends",
            data=data_json,
        )

        return response
        
    # Utility methods
    @staticmethod
    def _create_friends_connection_schema(
        payload: FriendSchema,
    ) -> FriendModelSchema:
        time_now_tz = get_datetime_now_melb()

        return FriendModelSchema(
            id=uuid.uuid4(),
            created_at=time_now_tz,
            updated_at=time_now_tz,
            is_deleted=False,

            friend_one=payload.friend_one,
            friend_two=payload.friend_two,
        )
    
    @classmethod
    def _create_friends_connection(
        cls,
        session: Session,
        payload: FriendSchema,
    ) -> Friend:
        friend_model_schema = cls._create_friends_connection_schema(
            payload=payload,
        )

        friend_obj_db = Friend(**friend_model_schema.model_dump())

        try:
            session.add(friend_obj_db)
            session.commit()
            session.refresh(friend_obj_db)

            return friend_obj_db
        except Exception as err:
            session.rollback()
            raise err
