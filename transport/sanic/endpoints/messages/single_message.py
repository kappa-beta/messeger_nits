from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException


class SingleMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, user_id: int, message_id, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        """
        Просмотр сообщения по его id
        """

        if token.get('user_id') != user_id:
            return await self.make_response_json(status=403)

        db_message = message_queries.get_message(session, user_id=user_id, message_id=message_id)
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)
