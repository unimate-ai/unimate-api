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

from src.event import messages as EventMessages
from src.event.schema import (
    EventSchema,
    EventModelSchema,
)
from src.event.model import (
    Event,
)

class EventService:
    # Business logic
    @classmethod
    def create_event(
        cls,
        session: Session,
        payload: EventSchema,
    ) -> GenericAPIResponseModel:
        try:
            event = cls._create_event(
                session=session,
                payload=payload,
            )

            data = payload

            data_json = jsonable_encoder(data)
            
            response = GenericAPIResponseModel(
                status=HTTPStatus.CREATED,
                message=EventMessages.CREATED_EVENT,
                data=data_json,
            )

            return response
        except Exception as err:
            raise err

    # Utility 
    @staticmethod
    def _create_event_schema(
        payload: EventSchema,
    ) -> EventModelSchema:
        time_now_tz = get_datetime_now_melb()
        
        return EventModelSchema(
            id=uuid.uuid4(),
            created_at=time_now_tz,
            updated_at=time_now_tz,
            is_deleted=False,

            name=payload.name,
            organizer=payload.organizer,
            is_campus_event=payload.is_campus_event,
            start_time=payload.start_time,
            end_time=payload.end_time,
            interests=payload.interests,
            location=payload.location,
            description=payload.description,
        )

    @classmethod
    def _create_event(
        cls,
        session: Session,
        payload: EventSchema,
    ) -> Event:
        event_model_schema = cls._create_event_schema(
            payload=payload,
        )

        event_obj_db = Event(**event_model_schema.model_dump())

        try:
            session.add(event_obj_db)
            session.commit()
            session.refresh(event_obj_db)

            return event_obj_db
        except Exception as err:
            session.rollback()
            raise err