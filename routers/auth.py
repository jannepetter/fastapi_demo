from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models import User
from utils.tokens import make_token_payloads, make_tokens

auth_router = APIRouter()


@auth_router.post("/login")
async def login(data: dict):

    username = data.get("username", None)
    password = data.get("password", None)
    if not username and not password:
        raise HTTPException(
            status_code=400, detail={"Username and password are required"}
        )

    user = await User.get_or_none(email=username)

    password_ok = False
    if user:
        password_ok = user.verify_password(password)

    if not password_ok:
        raise HTTPException(
            status_code=401, detail={"Username or password not correct."}
        )

    role_data, user_data = await make_token_payloads(user)

    access_token, refresh_token = make_tokens(user_data, role_data)
    response = JSONResponse({"access": access_token}, status_code=200)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=1 * 24 * 60 * 60,
        samesite="strict",
        secure=True,
    )
    return response
