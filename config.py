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
            "default": "postgres://postgres:postgres@localhost:5432/testdb"
            # "default": "sqlite://:memory:"
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
    # TORTOISE_ORM = {
    #     "connections": {
    #         # Dict format for connection
    #         "test": {
    #             "engine": "tortoise.backends.asyncpg",
    #             "credentials": {
    #                 "host": "localhost",
    #                 "port": "5432",
    #                 "user": "postgres",
    #                 "password": "postgres",
    #                 "database": "testdb",
    #             },
    #         },
    #         # Using a DB_URL string
    #         "test": "postgres://postgres:postgres@localhost:5432/testdb",
    #     },
    #     "apps": {
    #         "default": {
    #             "models": ["models"],
    #             # If no default_connection specified, defaults to 'default'
    #             "default_connection": "default",
    #         }
    #     },
    # }
