from sqlalchemy.ext.asyncio import AsyncSession

from repositories.favourite import FavouriteRepository
from repositories.file import FileRepository
from repositories.note import NoteRepository
from repositories.route import RouteRepository
from repositories.tag import TagRepository
from repositories.team import TeamRepository
from repositories.user import UserRepository


class RepositoryFactor:
    @staticmethod
    def get_repository(db_session: AsyncSession, repo_name: str):
        match repo_name:
            case "tag":
                return TagRepository(db_session)
            case "route":
                return RouteRepository(db_session)
            case "file":
                return FileRepository(db_session)
            case "user":
                return UserRepository(db_session)
            case "note":
                return NoteRepository(db_session)
            case "team":
                return TeamRepository(db_session)
            case "favourite":
                return FavouriteRepository(db_session)
            case _:
                raise ValueError(f"Unknown repository: {repo_name}")
