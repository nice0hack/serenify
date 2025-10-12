from datetime import timedelta
from os import name
import time
import jwt
from core.auth.jwt_auth import create_access_token, create_refresh_token
from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from schemas import STokenWithRefresh, SUserAuth, SUserOut, SUserTokenPayload, SUserRegister, STokenRefresh  # pyright: ignore[reportAttributeAccessIssue]
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel # pyright: ignore[reportAttributeAccessIssue]
from core.security import Security


class AuthController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def auth_user(self, auth: SUserAuth) -> STokenWithRefresh:
        auth_dict = auth.dict()

        result = await self.session.execute(
            select(UserModel)
            .where(
                or_(
                    UserModel.email == auth_dict["login"],
                    UserModel.login == auth_dict["login"],
                )
            )
        )
        user = result.scalars().first()

        if not user or not Security.verify_password(
            auth_dict["password"], user.password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")


        payload = {
            "login": user.login,
            "id": user.id,
            "role": user.role_id
        }
        if user.role_id == 1:
            print("CREAte add fkdfbmk")
            payload["doctor_id"] = user.doctor_id
            print(payload)

        return STokenWithRefresh(
            access_token=create_access_token(
                payload, timedelta(minutes=settings.access_token_expire_minutes)
            ),
            refresh_token=create_refresh_token(
                payload, timedelta(minutes=settings.refresh_token_expire_minutes)
            ),
        )

    async def get_me(self, user: SUserTokenPayload) -> SUserOut | None:
        stmt = (
            select(UserModel)
            .where(UserModel.login == user.login)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return SUserOut.model_validate(user)
    
    async def register_user(self, user: SUserRegister) -> STokenWithRefresh:
        from models import UserModel
        from core.security import Security

        existing_user = await self.session.execute(
            select(UserModel).where(
                or_(UserModel.login == user.login, UserModel.email == user.email)
            )
        )
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="User already exists")

        # Создаем нового пользователя
        new_user = UserModel(
            login=user.login,
            email=user.email,
            name=user.name, 
            password=Security.hash_password(user.password),
            role_id=2
        )
        self.session.add(new_user)
        await self.session.commit()
        
        return await self.auth_user(user)

    async def refresh_token(self, token: STokenRefresh) -> STokenWithRefresh:
        from core.auth.jwt_key_manager import JWTKeyManager

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
                options={"verify_aud": False},
            )

            return STokenWithRefresh(
                access_token=create_access_token(payload),
                refresh_token=create_refresh_token(payload),
            )
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            raise HTTPException(status_code=401, detail="Invalid or expired token")
