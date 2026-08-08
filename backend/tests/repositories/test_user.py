import pytest
from repositories.user import UserRepository


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"name": "name", "login": "login", "password": "password"}, id="true creation"
        ),
    ],
)
async def test_create_user(db_session, payload):
    user_repository = UserRepository(db_session)
    user = await user_repository.create(payload)
    await db_session.commit()
    await db_session.refresh(user)
    response = await user_repository.get_by_id(user.id)
    assert response.login == payload["login"]
    assert response.name == payload["name"]
    assert response.id is not None
