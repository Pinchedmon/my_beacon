from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.tag import TagReadSchema


class RouteSchema(BaseModel):
    """Общие поля маршрута."""

    name: str = Field(max_length=100)
    points: dict = Field(default_factory=dict)


class RouteCreateSchema(RouteSchema):
    """Вход POST /routes."""

    team_id: int
    tag_ids: list[int] = []

    model_config = ConfigDict(extra="forbid")


class RouteUpdateSchema(BaseModel):
    """Вход PATCH /routes/{id}."""

    name: str | None = Field(default=None, max_length=100)
    points: dict | None = None
    tag_ids: list[int] | None = None

    model_config = ConfigDict(extra="forbid")


class RouteReadSchema(RouteSchema):
    """Выход."""

    id: int
    team_id: int

    created_at: datetime
    updated_at: datetime

    tags: list[TagReadSchema] = []

    model_config = ConfigDict(from_attributes=True)
