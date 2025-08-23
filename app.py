from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.authentication import AuthenticationMiddleware
from utils.authentication import MyAuthBackend
from config import TORTOISE_ORM
import logging
from routers import admin_router, base_router, auth_router

app = FastAPI()
logging.basicConfig(level=logging.INFO)
register_tortoise(
    app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True
)

app.include_router(admin_router, prefix="/api/admin")
app.include_router(base_router, prefix="/api/base")
app.add_middleware(AuthenticationMiddleware, backend=MyAuthBackend())
app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
async def home():
    return "works"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
