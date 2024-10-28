import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.settings import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], uselist=False)  # отправитель
    receiver = relationship("User", foreign_keys=[receiver_id], uselist=False)  # получатель
