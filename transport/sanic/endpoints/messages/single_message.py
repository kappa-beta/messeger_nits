from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from api.response import ResponseMessageDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException


class SingleMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Просмотр сообщения по его id
        """

        # if token.get('user_id') != user_id:
        #     return await self.make_response_json(status=403)

        db_message = message_queries.get_message(session, message_id=message_id)
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Редактирование сообщения по его id
        """

        request_model = RequestPatchMessageDto(body)
        db_message = message_queries.patch_message(session, request_model, message_id=message_id)
        session.commit_session()
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Удаление сообщения по его id
        """

        db_message = message_queries.delete_message(session, message_id=message_id)
        session.commit_session()
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)
