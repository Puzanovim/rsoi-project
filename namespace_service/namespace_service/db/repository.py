from typing import List, Sequence
from uuid import UUID

from sqlalchemy import Column, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.future import select

from namespace_service.db.db_config import async_session
from namespace_service.db.models import Namespace, NamespaceToUser
from namespace_service.exceptions import NotFoundNamespace
from namespace_service.schemas import (
    InputNamespace,
    NamespaceModel,
    NamespaceUsers,
    UpdateNamespace,
    UserNamespace,
    UserNamespaces,
)


class NamespaceRepository:
    def __init__(self, session_factory: async_scoped_session) -> None:
        self._session_factory: async_scoped_session = session_factory

    async def get_namespaces(self) -> List[NamespaceModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Namespace))

        namespaces: Sequence[Namespace] = result.scalars().all()

        return [NamespaceModel.from_orm(namespace) for namespace in namespaces]

    async def get_namespace(self, namespace_id: UUID) -> NamespaceModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Namespace).where(Namespace.id == namespace_id))

            try:
                namespace: Namespace = result.scalar_one()
            except NoResultFound:
                raise NotFoundNamespace

        return NamespaceModel.from_orm(namespace)

    async def create_namespace(self, namespace: InputNamespace, owner_id: UUID) -> NamespaceModel:
        new_namespace = Namespace(**namespace.dict(), owner_id=owner_id)

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(new_namespace)
            await session.flush()
            await session.refresh(new_namespace)

        return NamespaceModel.from_orm(new_namespace)

    async def update_namespace(self, namespace_id: UUID, namespace: UpdateNamespace) -> NamespaceModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Namespace).where(Namespace.id == namespace_id).with_for_update())

            try:
                updated_namespace: Namespace = result.scalar_one()
            except NoResultFound:
                raise NotFoundNamespace

            for key, value in namespace.dict(exclude_unset=True).items():
                if hasattr(updated_namespace, key):
                    setattr(updated_namespace, key, value)

            await session.flush()
            await session.refresh(updated_namespace)

        return NamespaceModel.from_orm(updated_namespace)

    async def delete_namespace(self, namespace_id: UUID) -> None:
        try:
            await self.get_namespace(namespace_id)
        except NotFoundNamespace:
            raise

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            await session.execute(delete(Namespace).where(Namespace.id == namespace_id))

    async def get_user_namespaces(self, user_id: UUID) -> UserNamespaces:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(NamespaceToUser).where(NamespaceToUser.user_id == user_id))

        namespaces: Sequence[NamespaceToUser] = result.scalars().all()
        return UserNamespaces(namespaces=[namespace.namespace_id for namespace in namespaces])  # type: ignore

    async def get_namespace_users(self, namespace_id: UUID) -> NamespaceUsers:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(NamespaceToUser).where(NamespaceToUser.namespace_id == namespace_id))

        namespaces: Sequence[NamespaceToUser] = result.scalars().all()
        return NamespaceUsers(users=[namespace.user_id for namespace in namespaces])  # type: ignore

    async def get_namespace_user(self, user_id: UUID, namespace_id: UUID) -> UserNamespace:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(
                select(NamespaceToUser).where(
                    NamespaceToUser.user_id == user_id, NamespaceToUser.namespace_id == namespace_id
                )
            )

            try:
                namespace: NamespaceToUser = result.scalar_one()
            except NoResultFound:
                raise NotFoundNamespace

        return UserNamespace.from_orm(namespace)

    async def add_user_to_namespace(self, namespace_id: UUID, user_id: UUID) -> None:
        namespace_to_user = NamespaceToUser(namespace_id=namespace_id, user_id=user_id)

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(namespace_to_user)
            await session.flush()
            await session.refresh(namespace_to_user)

    async def delete_user_from_namespace(self, namespace_id: UUID, user_id: UUID) -> None:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            await session.execute(
                delete(NamespaceToUser).where(
                    NamespaceToUser.namespace_id == namespace_id, NamespaceToUser.user_id == user_id
                )
            )


namespace_repository: NamespaceRepository = NamespaceRepository(async_session)


def get_namespace_repo() -> NamespaceRepository:
    return namespace_repository
