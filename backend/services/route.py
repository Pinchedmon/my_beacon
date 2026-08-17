from sqlalchemy.ext.asyncio import AsyncSession

from schemas.route import RouteReadSchema


class RouteService:
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def create_route(self, route: RouteReadSchema) -> RouteReadSchema:
        pass

    async def delete_route(self, route: RouteReadSchema) -> RouteReadSchema:
        pass

    async def add_point_in_route(self):
        pass

    async def update_point_in_route(self):
        pass

    async def delete_point_in_route(self):
        pass
