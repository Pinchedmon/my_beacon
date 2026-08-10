from pydantic import BaseModel, ConfigDict, Field


class FileSchema(BaseModel):
    """Общие поля файла. minio_id — ключ объекта в S3/MinIO."""

    minio_id: str = Field(max_length=255)
    note_id: int | None = None
    favourite_id: int | None = None


class FileCreateSchema(FileSchema):
    """Вход POST /files."""

    model_config = ConfigDict(extra="forbid")


class FileUpdateSchema(BaseModel):
    """Вход PATCH /files/{id}."""

    minio_id: str | None = Field(default=None, max_length=255)
    note_id: int | None = None
    favourite_id: int | None = None

    model_config = ConfigDict(extra="forbid")


class FileReadSchema(FileSchema):
    """Выход."""

    id: int

    model_config = ConfigDict(from_attributes=True)
