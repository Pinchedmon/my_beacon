from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.file import FileReadSchema
from schemas.tag import TagReadSchema
from schemas.user import UserReadSchema


class FavouriteSchema(BaseModel):
    """Общие поля избранного."""

    name: str = Field(max_length=100)
    content: dict = Field(default_factory=dict)
    done: bool = False


class FavouriteCreateSchema(FavouriteSchema):
    """Вход POST /favourites."""

    team_id: int
    tag_ids: list[int] = []

    model_config = ConfigDict(extra="forbid")


class FavouriteUpdateSchema(BaseModel):
    """Вход PATCH /favourites/{id}."""

    name: str | None = Field(default=None, max_length=100)
    content: dict | None = None
    done: bool | None = None
    tag_ids: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class FavouriteReadSchema(FavouriteSchema):
    """Выход."""

    id: int
    team_id: int

    created_at: datetime
    updated_at: datetime

    tags: list[TagReadSchema] = []
    files: list[FileReadSchema] = []
    user_likes: list[UserReadSchema] = []

    model_config = ConfigDict(from_attributes=True)
