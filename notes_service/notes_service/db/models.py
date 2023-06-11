import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from notes_service.db.db_config import Base


class Note(Base):
    __tablename__ = 'note'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(80), nullable=False)
    text = Column(String, nullable=False)
    created_date = Column(TIMESTAMP, nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    namespace_id = Column(UUID(as_uuid=True), nullable=False)
