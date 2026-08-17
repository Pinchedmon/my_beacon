from sqlalchemy.ext.asyncio import AsyncSession

from schemas.favourite import FavouriteCreateSchema, FavouriteUpdateSchema


class FavouriteService:
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def add_favourite(self, favourite: FavouriteCreateSchema):
        pass

    async def update_favourite(self, favourite: FavouriteUpdateSchema):
        pass

    async def delete_favourite(self, favourite_id: int):
        pass
