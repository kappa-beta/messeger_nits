from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseMessageDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicMessageNotFound

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException, DBMessageNotExistsException


class SingleMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Просмотр сообщения по его id
        """

        if token.get('user_id') != message_queries.check_user_by_message_id(session, message_id=message_id).sender_id:
            return await self.make_response_json(status=403)

        # db_message = message_queries.get_message(session, message_id=message_id)
        try:
            db_message = message_queries.get_message(session, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Редактирование сообщения по его id
        """

        if token.get('user_id') != message_queries.check_user_by_message_id(session, message_id=message_id).sender_id:
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)
        # db_message = message_queries.patch_message(session, request_model, message_id=message_id)
        try:
            db_message = message_queries.patch_message(session, request_model, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
            **kwargs
    ) -> BaseHTTPResponse:
        """
        Удаление сообщения по его id
        """

        try:
            message_queries.delete_message(session, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        # response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body={}, status=201)
