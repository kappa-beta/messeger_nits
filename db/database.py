from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session, Query


from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    """
    Класс сессии подключения к БД.
    """
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        """
        Создание объекта запроса к БД с переданными параметрами.
        """
        return self._session.query(*args, **kwargs)

    def users(self) -> Query:
        return self.query(DBUser)

    def close_session(self):
        """
        Закрытие сессии
        """
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_user_by_login(self, login: str) -> DBUser:
        return self.users().filter(DBUser.login == login).first()

    def get_user_by_id(self, user_id: int) -> DBUser:
        return self.users().filter(DBUser.id == user_id).first()

    def get_user_all(self) -> List[DBUser]:
        qs = self.users()
        print(qs)
        return qs.all()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    """
    Базовый класс базы данных.
    """
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        """
        Инициализация функции создающей сессии на основе заданного подключения.
        """
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        """
        Проверка подключения к базе данных.
        """
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        """
        Создание сессии подключения к БД.
        """
        session = self.session_factory()
        return DBSession(session)
