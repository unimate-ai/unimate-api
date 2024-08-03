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

from src.account.model import User
from src.account.exceptions import (
    UnauthorizedOperationException,
    UserDoesNotExistsException
)
from src.account.service import AccountService


from src.chat.exceptions import (
    ChatroomAlreadyExistsException,
)

from src.chat.model import (
    Chatroom,
    ChatMessage
)
from src.chat.schema import (
    ChatroomRequestSchema,
    ChatroomSchema,
    ChatroomModelSchema,
    ChatMessageSchema,
    ChatMessageModelSchema,
)

class ChatService:
    # Business logic
    @classmethod
    def create_chatroom(
        cls,
        payload: ChatroomRequestSchema,
        current_user_email: EmailStr,
        session: Session,
    ) -> GenericAPIResponseModel:
        try:
            # Check if user is logged in
            user = AccountService.get_user_by_email(
                session=session,
                student_email=current_user_email,
            )

            if user is None:
                raise UnauthorizedOperationException()
            
            # Check if a chatroom with the intended users already exist or not
            room_participants = [user.id, payload.friend_id]

            # Filter for Chatrooms which contains the two users (meaning - an existing chatroom between both users)
            is_chatroom_exist = session.query(Chatroom) \
                                .filter(
                                    (
                                           (Chatroom.user_one_id == room_participants[0]) & \
                                            (Chatroom.user_two_id == room_participants[1])
                                    ) | (
                                           (Chatroom.user_one_id == room_participants[1]) & \
                                           (Chatroom.user_two_id == room_participants[0])
                                    )
                                ) \
                                .all()
            
            if len(is_chatroom_exist) > 0:
                raise ChatroomAlreadyExistsException()
            
            # If no duplicate is found, create new chatroom
            chatroom = cls._create_chatroom(
                user=user,
                session=session,
                payload=payload,
            )

            data = {
                "chatroom": chatroom,
            }

            data_json = jsonable_encoder(data)

            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message="Successfully created new chatroom",
                data=data_json,
            )

            return response
        except Exception as err:
            raise err
        
    # Utility methods
    @staticmethod
    def _create_chatroom_schema(
        payload: ChatroomRequestSchema,
        user: User,
    ) -> ChatroomModelSchema:
        time_now_tz = get_datetime_now_melb()

        return ChatroomModelSchema(
            id=uuid.uuid4(),
            created_at=time_now_tz,
            updated_at=time_now_tz,
            is_deleted=False,

            user_one_id=user.id,
            user_two_id=payload.friend_id,
        )
    
    @classmethod
    def _create_chatroom(
        cls,
        user: User,
        session: Session,
        payload: ChatroomSchema,
    ) -> Chatroom:
        chatroom_model_schema = cls._create_chatroom_schema(
            payload=payload,
            user=user,
        )

        chatroom_obj_db = Chatroom(**chatroom_model_schema.model_dump())
        
        try:
            session.add(chatroom_obj_db)
            session.commit()
            session.refresh(chatroom_obj_db)

            return chatroom_obj_db
        except Exception as err:
            session.rollback()
            raise err