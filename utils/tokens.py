from datetime import datetime, timedelta
import jwt
from config import JWT_SECRET

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
