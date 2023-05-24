import uuid

from category_service.db.db_config import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class Namespace(Base):
    __tablename__ = 'namespace'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)


class NamespaceToUser(Base):
    __tablename__ = 'namespace_to_user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    namespace_id = Column(UUID(as_uuid=True), nullable=False)
