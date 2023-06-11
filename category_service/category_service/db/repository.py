from typing import List, Sequence, Set
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.future import select

from category_service.db.db_config import async_session
from category_service.db.models import Category, CategoryToNote
from category_service.exceptions import NotFoundCategory
from category_service.schemas import CategoryModel, InputCategory


class CategoryRepository:
    def __init__(self, session_factory: async_scoped_session) -> None:
        self._session_factory: async_scoped_session = session_factory

    async def get_categories(self, namespace_id: UUID) -> List[CategoryModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Category).where(Category.namespace_id == namespace_id))

        categories: Sequence[Category] = result.scalars().all()

        return [CategoryModel.from_orm(category) for category in categories]

    async def get_category(self, category_id: UUID) -> CategoryModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            category_query = select(Category).where(Category.id == category_id)
            result = await session.execute(category_query)

            try:
                category: Category = result.scalar_one()
            except NoResultFound:
                raise NotFoundCategory

        return CategoryModel.from_orm(category)

    async def get_category_by_name(self, category_name: str) -> CategoryModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            category_query = select(Category).where(Category.name == category_name)
            result = await session.execute(category_query)

            try:
                category: Category = result.scalar_one()
            except NoResultFound:
                raise NotFoundCategory

        return CategoryModel.from_orm(category)

    async def create_category(self, category: InputCategory) -> CategoryModel:
        try:
            return await self.get_category_by_name(category.name)
        except NotFoundCategory:
            pass

        new_category = Category(**category.dict())

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(new_category)
            await session.flush()
            await session.refresh(new_category)

        return CategoryModel.from_orm(new_category)

    async def delete_category(self, category_id: UUID) -> None:
        try:
            await self.get_category(category_id)
        except NotFoundCategory:
            raise

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            category_query = delete(Category).where(Category.id == category_id)
            await session.execute(category_query)

    async def get_note_categories(self, note_id: UUID) -> List[CategoryModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(CategoryToNote).where(CategoryToNote.note_id == note_id))

        categories_to_notes: Sequence[CategoryToNote] = result.scalars().all()
        categories: List[CategoryModel] = []

        for category in categories_to_notes:
            category_model: CategoryModel = await self.get_category(category.category_id)  # type: ignore
            categories.append(category_model)

        return categories

    async def _check_note_has_category(self, category_id: UUID, note_id: UUID) -> bool:
        categories = await self.get_note_categories(note_id)

        for category in categories:
            if category.id == category_id:
                return True

        return False

    async def add_category_to_note(self, category_id: UUID, note_id: UUID) -> None:
        try:
            await self.get_category(category_id)
        except NotFoundCategory:
            raise

        if await self._check_note_has_category(category_id, note_id):
            return None

        category_to_note = CategoryToNote(category_id=category_id, note_id=note_id)

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(category_to_note)
            await session.flush()
            await session.refresh(category_to_note)

    async def delete_category_from_note(self, category_id: UUID, note_id: UUID) -> None:
        note_categories_ids: Set[UUID] = set([category.id for category in await self.get_note_categories(note_id)])

        if category_id not in note_categories_ids:
            raise NotFoundCategory

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            category_query = delete(CategoryToNote).where(
                CategoryToNote.category_id == category_id, CategoryToNote.note_id == note_id
            )
            await session.execute(category_query)


category_repository: CategoryRepository = CategoryRepository(async_session)


def get_category_repo() -> CategoryRepository:
    return category_repository
