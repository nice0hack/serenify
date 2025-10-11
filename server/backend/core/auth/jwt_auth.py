from datetime import datetime, timedelta, timezone
import jwt
from core.auth.jwt_key_manager import JWTKeyManager
from core.settings import settings

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(
        payload=to_encode,
        key=JWTKeyManager.get_private_key(),
        algorithm="RS256",
        headers={"kid": JWTKeyManager.get_kid()},
    )


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(minutes=10080)):
    to_encode = data.copy()
    to_encode.update({"exp":  datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(
        payload=to_encode,
        key=JWTKeyManager.get_private_key(),
        algorithm="RS256",
        headers={"kid": JWTKeyManager.get_kid()},
    )


async def decode_access_token(token: str, session):
    from models.jwt_key_model import JWTKeyModel
    from sqlalchemy import select
    from jwt import get_unverified_header, decode, InvalidTokenError

    headers = get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        raise InvalidTokenError("Missing kid")
    result = await session.execute(select(JWTKeyModel).where(JWTKeyModel.kid == kid))
    key = result.scalars().first()
    if not key:
        raise InvalidTokenError("Public key not found")
    return decode(token, key.public_key.encode(), algorithms=settings.jwt_algorithm)
