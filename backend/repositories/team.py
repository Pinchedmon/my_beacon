from logging import getLogger

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.user import User
from schemas.user import UserCreateSchema

logger = getLogger(__name__)


class TeamRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: UserCreateSchema) -> User:
        try:
            user = User(**payload.model_dump())
            self.db.add(user)
            await self.db.flush()
            return user

        except IntegrityError as exc:
            await self.db.rollback()
            logger.error(f"User with login {payload.login} already exists")
            raise ValueError(f"User with login {payload.login} already exists") from exc

        except SQLAlchemyError as exc:
            await self.db.rollback()
            logger.error(f"Failed to create user with login {payload.login}: {exc}")
            raise exc

    async def get_by_id(self, user_id: int) -> User | None:
        try:
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(
                    selectinload(User.teams),
                    selectinload(User.favourites),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as exc:
            logger.error(f"failed to get user with id {user_id}")
            raise exc

    async def get_all(self) -> list[User]:
        try:
            stmt = select(User).options(selectinload(User.teams), selectinload(User.favourites))
            result = await self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            logger.error("failed to get users")
            raise exc

    async def delete(self, user_id: int) -> None:
        try:
            stmt = delete(User).where(User.id == user_id)
            await self.db.execute(stmt)
        except SQLAlchemyError as exc:
            logger.error(f"failed to delete user with id {user_id}")
            raise exc
