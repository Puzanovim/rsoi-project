from typing import List, Sequence
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.future import select

from notes_service.db.db_config import async_session
from notes_service.db.models import Note
from notes_service.exceptions import NotFoundNote
from notes_service.schemas import InputNote, NoteModel, UpdateNote


class NoteRepository:
    def __init__(self, session_factory: async_scoped_session) -> None:
        self._session_factory: async_scoped_session = session_factory

    async def get_notes(self) -> List[NoteModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Note))

        notes: Sequence[NoteModel] = result.scalars().all()

        return [NoteModel.from_orm(note) for note in notes]

    async def get_namespace_notes(self, namespace_id: UUID) -> List[NoteModel]:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Note).where(Note.namespace_id == namespace_id))

        notes: Sequence[NoteModel] = result.scalars().all()

        return [NoteModel.from_orm(note) for note in notes]

    async def get_note(self, note_id: UUID) -> NoteModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Note).where(Note.id == note_id))

            try:
                note: Note = result.scalar_one()
            except NoResultFound:
                raise NotFoundNote

        return NoteModel.from_orm(note)

    async def create_note(self, note: InputNote) -> NoteModel:
        new_note = Note(**note.dict())

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            session.add(new_note)
            await session.flush()
            await session.refresh(new_note)

        return NoteModel.from_orm(new_note)

    async def update_note(self, note_id: UUID, note: UpdateNote) -> NoteModel:
        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            result = await session.execute(select(Note).where(Note.id == note_id).with_for_update())

            try:
                updated_note: Note = result.scalar_one()
            except NoResultFound:
                raise NotFoundNote

            for key, value in note.dict(exclude_unset=True).items():
                if hasattr(updated_note, key):
                    setattr(updated_note, key, value)

            await session.flush()
            await session.refresh(updated_note)

        return NoteModel.from_orm(updated_note)

    async def delete_note(self, note_id: UUID) -> None:
        try:
            await self.get_note(note_id)
        except NotFoundNote:
            raise

        session: AsyncSession = self._session_factory()
        async with session, session.begin():
            await session.execute(delete(Note).where(Note.id == note_id))


note_repository: NoteRepository = NoteRepository(async_session)


def get_note_repo() -> NoteRepository:
    return note_repository
