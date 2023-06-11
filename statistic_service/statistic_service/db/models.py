import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from statistic_service.db.db_config import Base


class Statistic(Base):
    __tablename__ = 'statistic'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service = Column(String(32), nullable=False)
    description = Column(String(512), nullable=False)
    created_time = Column(TIMESTAMP, nullable=False)
