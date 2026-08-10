from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    """Общие поля пользователя. Пароля здесь нет и быть не должно."""

    login: str = Field(min_length=3, max_length=255)
    name: str = Field(min_length=1, max_length=100)


class UserCreateSchema(UserSchema):
    """Вход POST /users. Пароль СЫРОЙ — это граница API."""

    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid")


class UserCreateDTO(UserSchema):
    """Вход UserRepository.create(). Пароль уже ХЕШИРОВАН."""

    password_hash: str


class UserUpdateSchema(BaseModel):
    """Вход PATCH /users/{id}. Не наследует UserSchema — иначе поля обязательны."""

    name: str | None = Field(default=None, min_length=1, max_length=100)

    model_config = ConfigDict(extra="forbid")


class UserReadSchema(UserSchema):
    """Выход. Пароля/хеша нет — и не добавляй."""

    id: int

    model_config = ConfigDict(from_attributes=True)
