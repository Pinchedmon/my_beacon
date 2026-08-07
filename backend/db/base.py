from core.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс таблицы БД."""

    def __repr__(self):
        table_columns = []
        for column in self.__table__.columns.keys():  # noqa: SIM118
            table_columns.append(f"{column}={getattr(self, column)}")
        return f"<{self.__class__.__name__} {', '.join(table_columns)}>"


# TODO: разобраться c pool_size, max_overflow, echo, pool_pre_ping
async_pg_engine = create_async_engine(Config.postgres_config.asyncpg_connection)
# TODO: разобраться c autoflush
AsyncSessionLocal = async_sessionmaker(async_pg_engine, expire_on_commit=False)


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
