import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserCreateSchema, UserReadSchema, UserUpdateSchema


class UserService:
    def __init__(self, db_session: AsyncSession, user_repo: UserRepository):
        self.db_session = db_session
        self.user_repo = user_repo

    async def create_user(self, payload: UserCreateSchema) -> UserReadSchema:
        hash_salt = bcrypt.gensalt(8)
        hashed_password = bcrypt.hashpw(payload.password.encode("utf-8"), hash_salt)
        user = await self.user_repo.create(
            password=hashed_password.decode("utf-8"), name=payload.name, login=payload.login
        )
        await self.db_session.commit()
        return UserReadSchema.model_validate(user)

    async def authenticate_user(self, payload: UserCreateSchema) -> UserReadSchema:
        pass

    async def verify_user(self, payload: UserCreateSchema) -> UserReadSchema:
        pass

    async def edit_user(self, payload: UserUpdateSchema) -> UserReadSchema:
        pass

    async def delete_user(self):
        pass
