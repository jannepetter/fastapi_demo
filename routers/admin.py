from fastapi import Request, APIRouter
from models import User
from serializers.user import UserRequestSerializer, UserResponseSerializer
from pydantic import ValidationError

admin_router = APIRouter()


@admin_router.get("/users")
async def get_users():
    users = await User.all().values("id", "name")
    return users


@admin_router.post("/users")
async def create_user(data: dict):
    try:
        validated = UserRequestSerializer.model_validate(data)
        user = User(**validated.model_dump())
        user.set_password(validated.password)
        await user.save()
    except ValidationError as e:
        error = e.errors()[0]
        return {"error": error["msg"]}

    return UserResponseSerializer(**user.__dict__)
