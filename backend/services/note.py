from sqlalchemy.ext.asyncio import AsyncSession

from schemas.note import NoteCreateSchema, NoteUpdateSchema


class NoteService:
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def add_note(self, note: NoteCreateSchema):
        pass

    async def delete_note(self, note_id: int):
        pass

    async def update_note(self, note_id: int, note: NoteUpdateSchema):
        pass
