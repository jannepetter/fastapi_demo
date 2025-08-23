from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse


class AdminLayerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/api/admin"):
            if not "admin" in request.auth.scopes:
                return JSONResponse({"detail": "Not authorized"}, status_code=403)

        response = await call_next(request)

        return response


class AuthLayerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, whitelist=[]):
        self.whitelist = whitelist
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        if (
            not request.user.is_authenticated
            and request.url.path.startswith("/api/")
            and not any(request.url.path.startswith(path) for path in self.whitelist)
        ):
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)
        response = await call_next(request)

        return response
