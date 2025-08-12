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

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user2(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users2(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user3(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users3(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ----


@pytest.mark.anyio
async def test_create_user4(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users4(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---
@pytest.mark.anyio
async def test_create_user5(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users5(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user5(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users5(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


@pytest.mark.anyio
async def test_create_user6(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users6(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user7(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users7(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user8(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users8(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ----


@pytest.mark.anyio
async def test_create_user9(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users9(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---
@pytest.mark.anyio
async def test_create_user10(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users10(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]


# ---


@pytest.mark.anyio
async def test_create_user11(client):
    name = await User.create(name="jussipuss2i")
    name.save().close()

    response = await client.get("/create_user")
    data = response.json()
    assert data == "Created user alice"

    response = await client.get("/create_user")

    response = await client.get("/users")

    data = response.json()

    assert data == [
        {"id": data[0]["id"], "name": "jussipuss2i"},
        {"id": data[1]["id"], "name": "alice"},
        {"id": data[2]["id"], "name": "alice"},
    ]


@pytest.mark.anyio
async def test_users11(client, user_fixture):

    response = await client.get("/users")
    data = response.json()
    assert len(data) == 3
    assert data == [
        {"id": data[0]["id"], "name": "John"},
        {"id": data[1]["id"], "name": "Mia"},
        {"id": data[2]["id"], "name": "jussipussi"},
    ]
