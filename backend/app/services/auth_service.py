from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


SECRET_KEY = settings.jwt_secret_key

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    user_id: int,
) -> str:

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def decode_access_token(
    token: str,
) -> int:

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    user_id = payload.get(
        "sub"
    )

    if not user_id:
        raise ValueError(
            "Invalid token"
        )

    return int(user_id)