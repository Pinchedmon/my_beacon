"""Корневые фикстуры для тестов."""

from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import config
from db.base import get_session
from db.models import User
from main import app
from repositories.user import UserRepository
from schemas.user import UserCreateSchema

BASE_DIR = Path(__file__).resolve().parent.parent

pg = config.postgres_config


@pytest.fixture(scope="session")
def test_database() -> Iterator[str]:
    """Создаёт тестовую БД до прогона и сносит её после."""
    name = pg.PG_DB_TEST
    if not name.endswith("_test"):
        raise RuntimeError(
            f"Имя тестовой БД должно оканчиваться на '_test', получено {name!r}. "
            "Проверь PG_DB_TEST — иначе тесты снесут рабочую базу."
        )

    # Отдельное синхронное подключение к служебной БД: CREATE/DROP DATABASE
    # нельзя выполнить ни внутри транзакции, ни будучи подключённым к самой БД.
    admin = create_engine(pg.admin_connection, isolation_level="AUTOCOMMIT")

    with admin.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{name}"'))

    yield name

    with admin.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
    admin.dispose()


@pytest.fixture(scope="session")
def migrated_database(test_database: str) -> str:
    """Накатывает alembic-миграции на тестовую БД."""
    alembic_cfg = AlembicConfig(str(BASE_DIR / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(BASE_DIR / "db" / "migrations"))
    alembic_cfg.set_main_option("sqlalchemy.url", pg.alembic_connection_test)
    command.upgrade(alembic_cfg, "head")
    return test_database


@pytest.fixture(scope="session")
async def engine(migrated_database: str) -> AsyncIterator[AsyncEngine]:
    async_engine = create_async_engine(pg.asyncpg_connection_test)
    yield async_engine
    await async_engine.dispose()


@pytest.fixture
async def connection(engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
    """Внешняя транзакция на тест: всё, что он записал, откатывается."""
    async with engine.connect() as conn:
        transaction = await conn.begin()
        yield conn
        await transaction.rollback()


@pytest.fixture
async def db_session(connection: AsyncConnection) -> AsyncIterator[AsyncSession]:
    # create_savepoint — чтобы session.commit() внутри тестируемого кода
    # закрывал SAVEPOINT, а не внешнюю транзакцию.
    session_factory = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def created_user(db_session: AsyncSession) -> User:
    """Создаёт пользователя, чтобы использовать его в тестах"""
    test_data_user = UserCreateSchema(name="testovich", login="tectovich", password="12341234")
    # test_data_team = Team(
    #     name="teamovich",
    # )
    user_repository = UserRepository(db_session)
    user = await user_repository.create(**test_data_user.model_dump())
    # user.teams.append(test_data_team)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as async_client:
            yield async_client
    finally:
        app.dependency_overrides.clear()
