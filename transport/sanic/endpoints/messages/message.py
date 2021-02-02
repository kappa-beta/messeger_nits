from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException


class MessageEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        """
        Создание сообщения
        """
        user_id = token.get('user_id')
        request_model = RequestCreateMessageDto(body)
        db_message = message_queries.create_message(session, request_model, user_id=user_id)

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        """
        Просмотр всех сообщений
        """
        user_id = token.get('user_id')
        db_messages = message_queries.get_messages(session, user_id=user_id)
        response_model = ResponseMessageDto(db_messages, many=True)

        return await self.make_response_json(body=response_model.dump(), status=201)
