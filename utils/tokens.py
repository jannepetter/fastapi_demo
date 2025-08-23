from datetime import datetime, timedelta
import jwt
from config import JWT_SECRET
from models import TenantUserRole

ALGORITHM = "HS256"


def make_tokens(user_data: dict, data: dict, access_exp=15, refresh_exp=1):

    access_payload = {
        "user": user_data,
        "data": data,
        "exp": datetime.now() + timedelta(minutes=access_exp),
    }
    at = jwt.encode(access_payload, JWT_SECRET, algorithm=ALGORITHM)

    refresh_payload = {
        "user": user_data,
        "exp": datetime.now() + timedelta(days=refresh_exp),
    }

    rt = jwt.encode(refresh_payload, JWT_SECRET, algorithm=ALGORITHM)

    return at, rt


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except Exception:
        return None


async def make_token_payloads(user):

    roles = (
        await TenantUserRole.filter(tenant_user__user_id=user.id)
        .select_related("role", "tenant_user")
        .values("role__name", "tenant_user__tenant_id")
    )

    role_data = {}
    for item in roles:
        if item["tenant_user__tenant_id"] in role_data:
            role_data[item["tenant_user__tenant_id"]].append(item["role__name"])
        else:
            role_data[item["tenant_user__tenant_id"]] = item["role__name"]

    user_roles = []
    if user.is_superuser:
        user_roles.append("admin")

    if user.is_staff:
        user_roles.append("staff")

    user_data = {"id": user.id, "roles": user_roles}

    return role_data, user_data
