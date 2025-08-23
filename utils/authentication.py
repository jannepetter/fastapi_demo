from fastapi import HTTPException, Request
from functools import wraps
from typing import Callable, List

from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    AuthCredentials,
    UnauthenticatedUser,
)
from utils.tokens import decode_token


class MyAuthenticatedUser(SimpleUser):

    def __init__(self, username: str, tenant_roles: dict) -> None:
        super().__init__(username)
        self.tenant_roles = tenant_roles

    def get_tenant_roles(self, tenant_id):
        return self.tenant_roles.get(tenant_id, [])


class MyAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):

        auth_header = conn.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return AuthCredentials([]), UnauthenticatedUser()

        token = auth_header.split(" ", 1)[1]

        decoded = decode_token(token)

        scopes = decoded["user"]["roles"]
        return AuthCredentials(scopes), MyAuthenticatedUser(
            "someusername", decoded["data"]
        )


def require_any_role(*roles: List[str]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                raise HTTPException(status_code=401, detail="Not authenticated")

            scopes = getattr(request, "auth", None)
            scopes = getattr(scopes, "scopes", []) if scopes else []

            if "admin" in scopes:
                return await func(*args, request=request, **kwargs)

            tenant_id = kwargs.get("tenant_id", None)
            if tenant_id:
                scopes.append(user.get_tenant_roles(tenant_id))

            if not any(role in scopes for role in roles):
                raise HTTPException(
                    status_code=403,
                    detail=f"Not authorized",
                )

            return await func(*args, request=request, **kwargs)

        return wrapper

    return decorator
