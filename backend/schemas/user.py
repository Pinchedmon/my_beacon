from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    login: str
    name: str


class UserCreateSchema(UserSchema):
    password: str

    model_config = ConfigDict(extra="forbid")


class UserReadSchema(UserSchema):
    id: int
