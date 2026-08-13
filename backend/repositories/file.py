from db.models.file import File
from repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    model = File
