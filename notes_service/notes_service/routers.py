from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from notes_service.auth import get_current_user, get_superuser
from notes_service.db.repository import NoteRepository, get_note_repo
from notes_service.kafka_producer import KafkaProducer, get_kafka_producer
from notes_service.schemas import InputNote, InputNoteFields, NoteModel, NotesPage, UserModel

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=NotesPage)
async def get_namespace_notes(
    namespace_id: UUID,
    page: int = 1,
    size: int = 100,
    repo: NoteRepository = Depends(get_note_repo),
    current_user: UserModel = Depends(get_current_user),
) -> NotesPage:
    notes: List[NoteModel] = await repo.get_namespace_notes(namespace_id)

    result_count = len(notes)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        notes = notes[lower_bound:upper_bound]

    return NotesPage(page=page, size=size, total_elements=result_count, items=notes)


@router.get('/{note_id}', status_code=status.HTTP_200_OK, response_model=NoteModel)
async def get_note(
    note_id: UUID,
    repo: NoteRepository = Depends(get_note_repo),
    current_user: UserModel = Depends(get_current_user),
) -> NoteModel:
    return await repo.get_note(note_id)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=NoteModel)
async def create_note(
    note: InputNoteFields,
    repo: NoteRepository = Depends(get_note_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_current_user),
) -> NoteModel:
    new_note: InputNote = InputNote(**note.dict(), author_id=current_user.id)
    note = await repo.create_note(new_note)
    await kafka.pull(f'Created note {note.title}')
    return note


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_note(
    note_id: UUID,
    repo: NoteRepository = Depends(get_note_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    note = await repo.get_note(note_id)
    await repo.delete_note(note_id)
    await kafka.pull(f'Deleted note {note.title}')
