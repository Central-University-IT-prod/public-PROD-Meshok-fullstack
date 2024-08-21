from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from typing import Any, Literal

import jwt

from core.config import settings

ALGORITHM = "HS256"


@dataclass
class JWTData:
    email: str
    issuer: str
    issued_at: datetime
    expire_at: datetime


def generate_jwt(
        email: str,
        issuer: str,
        expires_delta: timedelta = timedelta(weeks=4),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    jwt_data = {
        "sub": email,
        "iat": datetime.now(timezone.utc),
        "iss": issuer,
        "exp": expire
    }
    token = jwt.encode(
        jwt_data,
        key=settings.secret,
        algorithm=ALGORITHM
    )

    return token


def decode_jwt(
        token: str
) -> JWTData:
    decoded_jwt: dict[str, Any] = jwt.decode(
        jwt=token,
        key=settings.secret,
        algorithms=[ALGORITHM]
    )

    if (
            "sub" not in decoded_jwt
            or "iat" not in decoded_jwt
            or "exp" not in decoded_jwt
            or "iss" not in decoded_jwt
    ):
        raise jwt.PyJWTError

    jwt_data = JWTData(
        email=decoded_jwt["sub"],
        issuer=decoded_jwt["iss"],
        issued_at=datetime.fromtimestamp(
            decoded_jwt["iat"],
            tz=timezone.utc
        ),
        expire_at=datetime.fromtimestamp(
            decoded_jwt["exp"],
            tz=timezone.utc
        ),
    )

    return jwt_data
