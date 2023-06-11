import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from category_service.db.db_config import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
    namespace_id = Column(UUID(as_uuid=True), nullable=False)


class CategoryToNote(Base):
    __tablename__ = 'category_to_note'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(UUID(as_uuid=True), nullable=False)
