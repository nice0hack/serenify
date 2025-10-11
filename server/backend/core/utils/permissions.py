from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from schemas import SUserTokenPayload # pyright: ignore[reportAttributeAccessIssue]
from sqlalchemy import select
from core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth.jwt_key_manager import JWTKeyManager
from core.security import Security
from models import UserModel # pyright: ignore[reportAttributeAccessIssue]
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status

security = HTTPBearer()


def require_permission(permission_code: str):
    async def checker(user: SUserTokenPayload = Depends(get_current_user)):
        if permission_code not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return user

    return checker


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> SUserTokenPayload:
    print(credentials)
    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Missing kid in token")

        public_key = JWTKeyManager.get_public_key_by_kid(kid)
        if not public_key:
            raise HTTPException(status_code=401, detail="Unknown key ID (kid)")

        payload = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            options={"verify_aud": False},  # если не используешь audience
        )
        # Проверяем, что токен не истек
        if "exp" in payload and Security.is_token_expired(payload):
            raise HTTPException(status_code=401, detail="Token has expired")
        if not await exist_user_in_db(payload["id"], session):
            raise HTTPException(status_code=401, detail="User not found")
        return SUserTokenPayload(**payload)
    except (
        jwt.ExpiredSignatureError,
        jwt.DecodeError,
        jwt.InvalidTokenError,
        PyJWTError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


async def exist_user_in_db(user_id: int, session: AsyncSession) -> bool:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None