import pytest
from models import User


@pytest.fixture
async def user_fixture():
    await User.bulk_create([User(name="John"), User(name="Mia")])

    await User.create(name="jussipussi")


@pytest.mark.anyio
async def test_create_user(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = client.get("/create_user")

    response = client.get("/users")

    data = response.json()

    assert data == [
        {"id": 1, "name": "jussipuss2i"},
        {"id": 2, "name": "alice"},
        {"id": 3, "name": "alice"},
    ]


@pytest.mark.anyio
def test_users(client, user_fixture):

    response = client.get("/users")

    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Mia"},
        {"id": 3, "name": "jussipussi"},
    ]
