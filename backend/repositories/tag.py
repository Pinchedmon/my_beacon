from sqlalchemy import select

from db.models.tag import Tag
from repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    model = Tag

    async def get_by_name(self, name: str) -> Tag | None:
        stmt = select(Tag).where(Tag.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(self, name: str) -> Tag:
        tag = await self.get_by_name(name)
        if tag is not None:
            return tag
        return await self.create({name: name})
