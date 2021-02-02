from typing import List

from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, user_id: int) -> DBMessage:
    recipient_id = session.get_user_id_by_login(message.recipient)[0]

    new_message = DBMessage(
        message=message.message,
        sender_id=user_id,
        recipient_id=recipient_id,
    )

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, user_id: int) -> List['DBMessage']:
    return session.get_messages_all(user_id=user_id)
