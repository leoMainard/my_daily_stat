import datetime
import jwt
from routine.config.settings import settings


def _make_serializable(d: dict) -> dict:
    return {
        k: v.isoformat() if isinstance(v, datetime.datetime) else v
        for k, v in d.items()
    }


def create_session_token(user_dict: dict) -> str:
    payload = {
        "user": _make_serializable(user_dict),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=30),
    }
    return jwt.encode(payload, settings.SESSION_SECRET, algorithm="HS256")


def decode_session_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SESSION_SECRET, algorithms=["HS256"])
        return payload["user"]
    except jwt.PyJWTError:
        return None
