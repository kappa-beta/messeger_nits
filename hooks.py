from sqlalchemy import create_engine

from configs.config import ApplicationConfig
from context import Context
from db.database import DataBase


def init_db(config: ApplicationConfig, context: Context):
    """
    Инициализирует подключение к БД и передает его приложению.
    """
    engine = create_engine(
        config.database.url,
        pool_pre_ping=True,  # автоматическое восстановление подключения к БД
    )
    database = DataBase(connection=engine)
    database.check_connection()

    context.set('database', database)
