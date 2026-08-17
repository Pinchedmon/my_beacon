from sqlalchemy.ext.asyncio import AsyncSession

from schemas.file import FileCreateSchema, FileReadSchema


class StorageService:
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def add_file(self, file: FileCreateSchema) -> FileReadSchema:
        pass

    async def add_files(self, files: list[FileCreateSchema]) -> list[FileReadSchema]:
        pass

    async def delete_file(self, file: FileReadSchema) -> FileReadSchema:
        pass

    async def update_file(self, file: FileReadSchema) -> FileReadSchema:
        pass
