from pydantic import BaseModel, ConfigDict, Field

from schemas.favourite import FavouriteReadSchema
from schemas.note import NoteReadSchema
from schemas.route import RouteReadSchema
from schemas.user import UserReadSchema


class TeamSchema(BaseModel):
    """Общие поля команды."""

    name: str = Field(max_length=100)


class TeamCreateSchema(TeamSchema):
    """Вход POST /teams."""

    model_config = ConfigDict(extra="forbid")


class TeamUpdateSchema(BaseModel):
    """Вход PATCH /teams/{id}."""

    name: str | None = Field(default=None, max_length=100)

    model_config = ConfigDict(extra="forbid")


class TeamReadSchema(TeamSchema):
    """Выход для списка GET /teams — плоский, без вложенностей."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class TeamDetailReadSchema(TeamReadSchema):
    """Выход для GET /teams/{id} — команда со всем содержимым."""

    users: list[UserReadSchema] = []
    notes: list[NoteReadSchema] = []
    routes: list[RouteReadSchema] = []

    favourites: list[FavouriteReadSchema] = []

    model_config = ConfigDict(from_attributes=True)
