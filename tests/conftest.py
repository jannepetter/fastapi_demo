import os
import uuid
import pytest
from tortoise import Tortoise
from tortoise.transactions import in_transaction
from httpx import ASGITransport, AsyncClient
from freezegun import freeze_time

worker_id = os.getenv("PYTEST_XDIST_WORKER", "gw0")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_URL = f"postgres://postgres:postgres@{DB_HOST}:5432/testdb_{worker_id}"


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url=DB_URL, modules={"models": ["models", "aerich.models"]}, _create_db=True
    )
    await Tortoise.generate_schemas(safe=False)
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def client():
    os.environ.setdefault("DATABASE_URL", DB_URL)
    from app import app  # pylint:disable=import-outside-toplevel

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def db_transaction(request):
    async with in_transaction() as conn:
        try:
            yield conn
            await conn.rollback()
        except:
            await conn.rollback()
            raise


@pytest.fixture(autouse=True)
def frozen_time():
    """Freeze time at a fixed point for tests."""
    with freeze_time("2025-08-23 12:00:00") as frozen:
        yield frozen
