from sqlalchemy import Column, Integer, BOOLEAN, NVARCHAR, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):
    __tablename__ = 'message'

    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(NVARCHAR(), nullable=False)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)
