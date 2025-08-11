import pytest
from tortoise.contrib.test import finalizer, initializer

# from fastapi.testclient import TestClient
from app import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "postgres://postgres:postgres@localhost:5432/testdb"
    initializer(["models"], db_url=db_url)
    request.addfinalizer(finalizer)


@pytest.fixture(scope="function", autouse=True)
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
