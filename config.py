import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL")

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
    TORTOISE_ORM = {
        "connections": {
            # "default": "postgres://postgres:postgres@localhost:5432/testdb"
            "default": "sqlite://:memory:"
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
