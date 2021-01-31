from sqlalchemy import Column, VARCHAR, VARBINARY

from db.models import BaseModel


class DBUser(BaseModel):
    __tablename__ = 'user'

    login = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARBINARY(), nullable=False)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
