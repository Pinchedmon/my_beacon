from sqlalchemy.ext.asyncio import AsyncSession

from repositories.repositories_factory import RepositoryFactor


def get_repository(db_session: AsyncSession, repo_name: str):
    return RepositoryFactor.get_repository(db_session, repo_name)
