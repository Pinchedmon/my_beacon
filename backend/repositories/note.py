from db.models.note import Note
from repositories.base import BaseRepository


class NoteRepository(BaseRepository[Note]):
    model = Note
