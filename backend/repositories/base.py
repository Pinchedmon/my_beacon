from logging import getLogger
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import _AbstractLoad

from db.base import Base

logger = getLogger(__name__)


class BaseRepository[ModelT: Base]:
    """Общий CRUD для всех сущностей."""

    model: type[ModelT]
    load_options: tuple[_AbstractLoad, ...] = ()

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data) -> ModelT:
        obj = self.model(**data)
        self.db.add(obj)
        # flush отправляет INSERT и заполняет id, но транзакцию не закрывает.
        # Без него вызывающий получит объект с id = None.
        await self.db.flush()
        return obj

    async def get_by_id(self, obj_id: int) -> ModelT | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        if self.load_options:
            stmt = stmt.options(*self.load_options)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        stmt = select(self.model).limit(limit).offset(offset)
        if self.load_options:
            stmt = stmt.options(*self.load_options)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(self, obj_id: int, data: dict[str, Any]) -> ModelT | None:
        obj = await self.get_by_id(obj_id)
        if obj is None:
            return None
        for field, value in data.items():
            setattr(obj, field, value)
        await self.db.flush()
        return obj

    async def delete(self, obj_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.db.execute(stmt)
