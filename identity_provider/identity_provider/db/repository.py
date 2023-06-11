from typing import List, Sequence
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.future import select

from identity_provider.config import pwd_context
from identity_provider.db.db_config import async_session
from identity_provider.db.models import User
from identity_provider.exceptions import NotFoundUser
from identity_provider.schemas import InputUser, UpdateUser, UserDB, UserModel


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class UserRepository:
    def __init__(self, session_factory: async_scoped_session) -> None:
        self._session_factory: async_scoped_session = session_factory

    async def get_users(self) -> List[UserModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(User))

        users: Sequence[User] = result.scalars().all()

        return [UserModel.from_orm(user) for user in users]

    async def get_user(self, user_id: UUID) -> UserModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(User).where(User.id == user_id))

            try:
                user: User = result.scalar_one()
            except NoResultFound:
                raise NotFoundUser

        return UserModel.from_orm(user)

    async def get_user_by_username(self, username: str) -> UserDB:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(User).where(User.username == username))

            try:
                user: User = result.scalar_one()
            except NoResultFound:
                raise NotFoundUser

        return UserDB.from_orm(user)

    async def create_user(self, user: InputUser) -> UserModel:
        try:
            return await self.get_user_by_username(user.username)
        except NotFoundUser:
            pass

        new_user = User(**user.dict(exclude={'password'}), hashed_password=get_password_hash(user.password))

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)

        return UserModel.from_orm(new_user)

    async def update_user(self, user_id: UUID, user: UpdateUser) -> UserModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(User).where(User.id == user_id).with_for_update())

            try:
                updated_namespace: User = result.scalar_one()
            except NoResultFound:
                raise NotFoundUser

            for key, value in user.dict(exclude_unset=True).items():
                if hasattr(updated_namespace, key):
                    setattr(updated_namespace, key, value)

            await session.flush()
            await session.refresh(updated_namespace)

        return UserModel.from_orm(updated_namespace)

    async def delete_user(self, user_id: UUID) -> None:
        try:
            await self.get_user(user_id)
        except NotFoundUser:
            raise

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            await session.execute(delete(User).where(User.id == user_id))


user_repository: UserRepository = UserRepository(async_session)


def get_user_repo() -> UserRepository:
    return user_repository
