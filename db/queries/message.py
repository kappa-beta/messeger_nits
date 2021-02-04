from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto

from db.exceptions import DBUserNotExistsException, DBMessageNotExistsException

from db.database import DBSession
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, user_id: int) -> DBMessage:
    try:
        recipient_id = session.get_user_id_by_login(message.recipient)
    except Exception:
        raise DBUserNotExistsException

    new_message = DBMessage(
        message=message.message,
        sender_id=user_id,
        recipient_id=recipient_id,
    )

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, user_id: int) -> List['DBMessage']:
    return session.get_messages_all(user_id=user_id)


def get_message(session: DBSession, message_id: int):
    try:
        db_message = session.get_message_single(message_id=message_id)
    except Exception:
        raise DBMessageNotExistsException
    return db_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int):
    try:
        db_message = session.get_message_single(message_id=message_id)
        for attr in message.fields:
            if hasattr(message, attr):
                value = getattr(message, attr)
                setattr(db_message, attr, value)
    except Exception:
        raise DBMessageNotExistsException
    return db_message


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    try:
        db_message = session.get_message_single(message_id=message_id)
        db_message.is_delete = True
    except Exception:
        raise DBMessageNotExistsException

    return db_message


def check_user_by_message_id(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_single(message_id=message_id)
    return db_message
