"""Юнит-тесты UserService: без БД, без сети, без миграций.

Сервис зависит от репозитория и сессии через __init__, поэтому в тесте
подставляем вместо них заглушки. Проверяем ЛОГИКУ СЕРВИСА (что он хеширует
пароль, что прокидывает поля, что коммитит), а не то, умеет ли SQLAlchemy
писать в Postgres — это забота интеграционных тестов в tests/repositories/.
"""

import bcrypt
import pytest

from db.models import User
from schemas.user import UserCreateSchema, UserReadSchema
from services.user import UserService

RAW_PASSWORD = "super-secret-123"


class FakeUserRepository:
    """Заглушка репозитория: ничего не пишет, только запоминает вызов."""

    def __init__(self):
        self.create_calls: list[dict] = []

    async def create(self, **data) -> User:
        self.create_calls.append(data)
        user = User(**data)
        # Настоящий репозиторий получает id из flush(). Здесь подделываем,
        # потому что UserReadSchema требует id: int.
        user.id = 1
        return user


class FakeSession:
    """Заглушка сессии: считает коммиты."""

    def __init__(self):
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


@pytest.fixture
def repo() -> FakeUserRepository:
    return FakeUserRepository()


@pytest.fixture
def session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def service(session: FakeSession, repo: FakeUserRepository) -> UserService:
    return UserService(db_session=session, user_repo=repo)  # type: ignore[arg-type]


@pytest.fixture
def payload() -> UserCreateSchema:
    return UserCreateSchema(login="alex", name="Алексей", password=RAW_PASSWORD)


async def test_password_is_hashed_not_stored_raw(service, repo, payload):
    """Сырой пароль не должен доехать до репозитория."""
    await service.create_user(payload)

    stored = repo.create_calls[0]["password"]
    assert stored != RAW_PASSWORD
    assert stored.startswith("$2b$")


async def test_hash_is_verifiable_by_bcrypt(service, repo, payload):
    """Главный тест: хеш должен реально матчиться при будущем логине.

    Ловит классический баг str(hashed) вместо hashed.decode() — там строка
    выглядит как хеш, но начинается с b'... и checkpw возвращает False.
    """
    await service.create_user(payload)

    stored = repo.create_calls[0]["password"]
    assert bcrypt.checkpw(RAW_PASSWORD.encode("utf-8"), stored.encode("utf-8"))


async def test_wrong_password_does_not_verify(service, repo, payload):
    """Обратная сторона: чужой пароль матчиться не должен."""
    await service.create_user(payload)

    stored = repo.create_calls[0]["password"]
    assert not bcrypt.checkpw(b"wrong-password", stored.encode("utf-8"))


async def test_login_and_name_passed_through(service, repo, payload):
    await service.create_user(payload)

    call = repo.create_calls[0]
    assert call["login"] == payload.login
    assert call["name"] == payload.name
    assert set(call) == {"login", "name", "password"}


async def test_commits_once(service, session, payload):
    await service.create_user(payload)

    assert session.commits == 1


async def test_returns_read_schema_without_password(service, payload):
    result = await service.create_user(payload)

    assert isinstance(result, UserReadSchema)
    assert result.login == payload.login
    assert result.name == payload.name
    assert result.id == 1
    # Пароля/хеша в ответе быть не должно — схема на выход его не содержит.
    assert not hasattr(result, "password")


async def test_salt_is_random_per_user(service, repo, payload):
    """Два одинаковых пароля дают разные хеши — соль генерится каждый раз."""
    await service.create_user(payload)
    await service.create_user(payload)

    first, second = (call["password"] for call in repo.create_calls)
    assert first != second
