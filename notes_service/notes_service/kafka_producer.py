import logging
from typing import Dict

from httpx import AsyncClient

from notes_service.config import KAFKA_CONFIG
from notes_service.schemas import StatisticMessage
from notes_service.validators import json_dump

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, topic: str):
        self._topic: str = topic
        self._host: str = 'statistic_service'
        self._port: int = 8040

    async def pull(self, message: str) -> None:
        statistic_message: StatisticMessage = StatisticMessage(service=self._topic, description=message)
        body: Dict = json_dump(statistic_message.dict())

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/statistics', json=body)

            try:
                response = await func
            except Exception as exc:
                logger.warning(f'Message to Statistic Service has not been sent: {exc}')
            else:
                if response.status_code != 201:
                    logger.info(f'Statistic Service return error: {response}')
                else:
                    logger.info('Message to Statistic Service sent')


kafka_producer = KafkaProducer(**KAFKA_CONFIG.dict())


async def get_kafka_producer() -> KafkaProducer:
    return kafka_producer
