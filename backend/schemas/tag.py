from pydantic import BaseModel, ConfigDict, Field


class TagSchema(BaseModel):
    """Общие поля тега. Без id, без связей — только то, что задаёт клиент."""

    name: str = Field(max_length=255)


class TagCreateSchema(TagSchema):
    """Вход POST /tags."""

    model_config = ConfigDict(extra="forbid")


class TagUpdateSchema(BaseModel):
    """Вход PATCH /tags/{id}."""

    name: str | None = Field(default=None, max_length=255)

    model_config = ConfigDict(extra="forbid")


class TagReadSchema(TagSchema):
    """Выход. Строится из ORM-объекта Tag."""

    id: int

    model_config = ConfigDict(from_attributes=True)
