from sqlalchemy.ext.asyncio import AsyncSession

from schemas.team import TeamReadSchema


class TeamService:
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def create_team(self) -> TeamReadSchema:
        pass

    async def update_team(self, team: TeamReadSchema) -> TeamReadSchema:
        pass

    async def join_team(self, team: TeamReadSchema) -> TeamReadSchema:
        pass

    async def leave_team(self, team: TeamReadSchema) -> TeamReadSchema:
        pass
