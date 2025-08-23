import pytest
from models import User


@pytest.fixture
async def user_fixture():
    await User.bulk_create(
        [
            User(name="John", email="juu@juu.fi", password="jeps"),
            User(name="Mia", email="juu2@juu.fi", password="jeps"),
        ]
    )

    await User.create(name="jussipussi", email="juu3@juu.fi", password="jeps")


@pytest.mark.anyio
async def test_users(client, user_fixture):

    response = await client.get("/api/admin/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


@pytest.mark.anyio
async def test_users12(
    client,
):
    user_data = {"email": "test@test.fi", "name": "testuser", "password": "passu"}
    response = await client.post("/api/admin/users", json=user_data)
    data = response.json()
    assert data == {"error": "Value error, Password must be at least 8 characters long"}


@pytest.mark.anyio
async def test_users13(
    client,
):
    user_data = {"email": "test@test.fi", "name": "testuser", "password": "passu" * 30}
    response = await client.post("/api/admin/users", json=user_data)
    data = response.json()
    assert data == {"error": "Value error, Password must be at max 128 characters long"}


@pytest.mark.anyio
async def test_users14(
    client,
):
    user_data = {
        "email": "test@test.fi",
        "name": "testuser",
        "password": "passu_long_enough",
    }
    response = await client.post("/api/admin/users", json=user_data)
    data = response.json()

    assert data == {"id": data["id"], "name": "testuser"}
    user = await User.get(email="test@test.fi")

    assert user.password != "passu_long_enough"
    assert len(user.password) == 97
