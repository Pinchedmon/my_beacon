from logging import getLogger

from db.models.user import User
from schemas.user import UserCreateSchema, UserReadSchema
from sqlalchemy.ext.asyncio import AsyncSession

logger = getLogger(__name__)


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: UserCreateSchema) -> UserReadSchema:
        try:
            user = User(**payload)
            self.db.add(user)
            return user
        except Exception:
            await self.db.rollback()
            logger.error(f"failed to create user with login {payload}")
            raise

    async def get_by_id(self, user_id: int) -> UserReadSchema:
        try:
            user = await self.db.get(User, user_id)
            return user
        except Exception:
            raise
            """TODO"""
            # logger.error(f"failed to create user with login{payload.login}")
