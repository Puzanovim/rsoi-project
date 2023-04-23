import uuid

from category_service.db.db_config import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class Category(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
