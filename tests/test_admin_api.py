import pytest
from models import User
from tests.tools import generate_auth_headers


@pytest.fixture
async def user_fixture():
    await User.bulk_create(
        [
            User(name="John", email="juu@juu.fi", password="jeps"),
            User(name="Mia", email="juu2@juu.fi", password="jeps"),
        ]
    )

    await User.create(name="jussipussi", email="juu3@juu.fi", password="jeps")
    admin_user = User(name="testadmin", email="juu4@juu.fi", is_superuser=True)
    admin_user.set_password("jeps")
    await admin_user.save()

    headers = await generate_auth_headers(admin_user)
    return {"headers": headers}


@pytest.mark.anyio
async def test_users(client, user_fixture):

    headers = user_fixture["headers"]
    response = await client.get("/api/admin/users", headers=headers)
    data = response.json()

    assert len(data) == 4
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
        {"id": data[3]["id"], "name": "testadmin"},
    ]


@pytest.mark.anyio
async def test_users12(client, user_fixture):
    user_data = {"email": "test@test.fi", "name": "testuser", "password": "passu"}

    headers = user_fixture["headers"]
    response = await client.post("/api/admin/users", json=user_data, headers=headers)
    data = response.json()
    assert data == {"error": "Value error, Password must be at least 8 characters long"}


@pytest.mark.anyio
async def test_users13(client, user_fixture):
    user_data = {"email": "test@test.fi", "name": "testuser", "password": "passu" * 30}

    headers = user_fixture["headers"]

    response = await client.post("/api/admin/users", json=user_data, headers=headers)
    data = response.json()
    assert data == {"error": "Value error, Password must be at max 128 characters long"}


@pytest.mark.anyio
async def test_users14(client, user_fixture):
    user_data = {
        "email": "test@test.fi",
        "name": "testuser",
        "password": "passu_long_enough",
    }

    headers = user_fixture["headers"]
    response = await client.post("/api/admin/users", json=user_data, headers=headers)
    data = response.json()

    assert data == {"id": data["id"], "name": "testuser"}
    user = await User.get(email="test@test.fi")

    assert user.password != "passu_long_enough"
    assert len(user.password) == 97


@pytest.mark.anyio
async def test_post_user_with_anonymous(client, user_fixture):
    user_data = {
        "email": "test@test.fi",
        "name": "testuser",
        "password": "passu_long_enough",
    }

    response = await client.post("/api/admin/users", json=user_data)
    data = response.json()
    assert response.status_code == 401
    assert data == {"detail": "Not authenticated"}
