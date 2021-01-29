from sanic import Sanic

from configs.config import ApplicationConfig
from context import Context
from hooks import init_db
from transport.sanic.routes import get_routes


def configure_app(config: ApplicationConfig, context: Context):
    """
    Экземпляр класса Sanic с настройками
    :param config: класс ApplicationConfig, содержащий настройки приложения.
    :param context: класс, содержащий подключение к БД.
    :return: объект Sanic
    """
    init_db(config, context)

    app = Sanic(__name__)

    for handler in get_routes(config, context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True,
        )

    return app
