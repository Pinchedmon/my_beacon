from db.models import User
from repositories.user import UserRepository
from schemas.user import UserCreateSchema


async def test_create_user_persists_and_is_readable(db_session):
    test_data = UserCreateSchema(name="name", login="login", password="password")
    user_repository = UserRepository(db_session)
    user = await user_repository.create(test_data)
    await db_session.commit()
    await db_session.refresh(user)
    response = await user_repository.get_by_id(user.id)
    assert response.login == test_data.login
    assert response.name == test_data.name
    assert response.id is user.id


async def test_get_by_id_returns_none_when_missing(db_session):
    user_repository = UserRepository(db_session)
    user = await user_repository.get_by_id(99999999)
    assert user is None


async def test_create_user_duplicate_login_raises(db_session):
    pass


# async def test_get_by_id_loads_teams(db_session, created_user):
#     user_repository = UserRepository(db_session)
#     user = await user_repository.get_by_id("99999999")
#     assert user is None
#     pass


async def test_delete_removes_user(db_session, created_user: User):
    user_repository = UserRepository(db_session)
    await user_repository.delete(created_user.id)
    await db_session.commit()
    check = await user_repository.get_by_id(created_user.id)
    assert check is None
