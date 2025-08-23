from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    AuthCredentials,
    requires,
)
from utils.tokens import decode_token


class MyAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        auth_header = conn.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # no auth → anonymous

        token = auth_header.split(" ", 1)[1]

        decoded = decode_token(token)
        # print("decodd--", decoded)
        # if not user_info:
        #     raise AuthenticationError("Invalid token or user not found")

        # Create Starlette user + scopes
        # user = SimpleUser("joo")
        # scopes = ["authenticated"]
        scopes = ["jepulis"]
        return AuthCredentials(scopes), SimpleUser("joo")
