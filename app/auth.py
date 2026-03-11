from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.core.config import settings

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

PASSWORD_HASH = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return PASSWORD_HASH.hash(password)

def check_password(plain_password: str, hashed_password: str):
    return PASSWORD_HASH.verify(plain_password, hashed_password)

def create_token(data: dict) -> dict:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(UTC) + timedelta(minutes=settings.token_expire_minutes)})

    return jwt.encode(
        payload=to_encode,
        key=settings.secret_key.get_secret_value(),
        algorithm=settings.alghorithm,
    )

def verify_token(token: str) -> str | None:
    try:
        decode_jwt = jwt.decode(
            jwt=token,
            key=settings.secret_key.get_secret_value(),
            algorithms=[settings.alghorithm],
            options={"require": ["exp", "sub"]},
        )
    except jwt.DecodeError:
        return None
    else:
        return decode_jwt.get("sub")
