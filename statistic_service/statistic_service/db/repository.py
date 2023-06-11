from typing import List, Sequence
from uuid import UUID

from sqlalchemy import Select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.future import select

from statistic_service.db.db_config import async_session
from statistic_service.db.models import Statistic
from statistic_service.exceptions import NotFoundStatistic
from statistic_service.schemas import InputStatistic, StatisticFilter, StatisticModel


class StatisticRepository:
    def __init__(self, session_factory: async_scoped_session) -> None:
        self._session_factory: async_scoped_session = session_factory

    async def get_statistics(self, statistic_filter: StatisticFilter) -> List[StatisticModel]:
        query: Select = select(Statistic)

        if statistic_filter.service:
            query = query.where(Statistic.service == statistic_filter.service)
        if statistic_filter.start_time:
            query = query.where(Statistic.created_time >= statistic_filter.start_time)
        if statistic_filter.finish_time:
            query = query.where(Statistic.created_time <= statistic_filter.finish_time)

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(query)

        statistics: Sequence[Statistic] = result.scalars().all()

        return [StatisticModel.from_orm(statistic) for statistic in statistics]

    async def get_statistic(self, statistic_id: UUID) -> StatisticModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Statistic).where(Statistic.id == statistic_id))

            try:
                statistic: Statistic = result.scalar_one()
            except NoResultFound:
                raise NotFoundStatistic

        return StatisticModel.from_orm(statistic)

    async def add_statistic(self, statistic: InputStatistic) -> StatisticModel:
        new_statistic = Statistic(**statistic.dict())

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(new_statistic)
            await session.flush()
            await session.refresh(new_statistic)

        return StatisticModel.from_orm(new_statistic)

    async def delete_statistic(self, statistic_id: UUID) -> None:
        try:
            await self.get_statistic(statistic_id)
        except NotFoundStatistic:
            raise

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            await session.execute(delete(Statistic).where(Statistic.id == statistic_id))


statistic_repository: StatisticRepository = StatisticRepository(async_session)


def get_statistic_repo() -> StatisticRepository:
    return statistic_repository
