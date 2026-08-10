from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.file import FileReadSchema
from schemas.tag import TagReadSchema


class NoteSchema(BaseModel):
    """Общие поля заметки."""

    name: str = Field(max_length=100)

    content: dict = Field(default_factory=dict)


class NoteCreateSchema(NoteSchema):
    """Вход POST /notes."""

    team_id: int

    tag_ids: list[int] = []

    model_config = ConfigDict(extra="forbid")


class NoteUpdateSchema(BaseModel):
    """Вход PATCH /notes/{id}."""

    name: str | None = Field(default=None, max_length=100)
    content: dict | None = None
    tag_ids: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class NoteReadSchema(NoteSchema):
    """Выход."""

    id: int
    team_id: int

    created_at: datetime
    updated_at: datetime
    tags: list[TagReadSchema] = []
    files: list[FileReadSchema] = []

    model_config = ConfigDict(from_attributes=True)
