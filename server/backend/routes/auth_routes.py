from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.permissions import get_current_user
from routes.base_routes import BaseRoutes # pyright: ignore[reportAttributeAccessIssue]
from core.utils.register_router import register_router
from controllers import AuthController # pyright: ignore[reportAttributeAccessIssue]
from schemas import STokenWithRefresh, SUserAuth, SUserRegister, SUserTokenPayload, STokenRefresh, SUserOut # pyright: ignore[reportAttributeAccessIssue]
from core.db import get_session


@register_router
class AuthRoutes(BaseRoutes):

    tag = "Auth"

    def _register_routes(self):
        @self.router.post('/auth/', response_model=STokenWithRefresh | None, tags=[self.tag])
        async def auth_user(auth: SUserAuth, session: AsyncSession = Depends(get_session)) -> dict:
            return await AuthController(session=session).auth_user(auth)

        @self.router.post('/refresh/', response_model=STokenWithRefresh | None, tags=[self.tag])
        async def refresh_token(token: STokenRefresh, session: AsyncSession = Depends(get_session)) -> STokenWithRefresh | None:
            return await AuthController(session=session).refresh_token(token)

        @self.router.post('/register/', response_model=STokenWithRefresh | None, tags=[self.tag])
        async def register_user(user: SUserRegister, session: AsyncSession = Depends(get_session)) -> STokenWithRefresh | None:
            return await AuthController(session=session).register_user(user)

        @self.router.get('/me/', response_model=SUserOut | None, tags=[self.tag])
        async def get_user_by_token( user: SUserTokenPayload = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> SUserTokenPayload | None:
            return await AuthController(session=session).get_me(user)
