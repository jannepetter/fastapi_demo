import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET", "testsecret")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

if ENV == "TEST":
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    TORTOISE_ORM = {
        "connections": {
            "default": f"postgres://postgres:postgres@localhost:5432/testdb_{worker_id}"
        },
        "apps": {
            "models": {
                "models": [
                    "models",
                    "aerich.models",
                ],
                "default_connection": "default",
            },
        },
    }
