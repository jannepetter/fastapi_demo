import pytest
from tortoise.contrib.test import finalizer, initializer
from fastapi.testclient import TestClient
from app import app


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "sqlite://:memory:"
    initializer(["models"], db_url=db_url)
    request.addfinalizer(finalizer)


@pytest.fixture(scope="function", autouse=True)
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
