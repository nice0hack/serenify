from fastapi import HTTPException, status, Depends
from dishka.integrations.fastapi import FromDishka, inject
from controllers import RoleController
from schemas import SRole, SRoleInDB, SUserTokenPayload
from core.utils.permissions import require_permission
from core.utils.register_router import register_router
from routes.base_routes import BaseRoutes
from core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

@register_router
class RoleRoutes(BaseRoutes):
    tag = "Roles"

    def _register_routes(self):
        @self.router.get('/roles/', response_model=list[SRoleInDB], tags=[self.tag])
        @inject
        async def get_roles( session: AsyncSession = Depends(get_session)) -> list[SRoleInDB]:
            controller = RoleController(session = session)
            return await controller.get_all()
        
        @self.router.get("/roles/{role_id}", tags=[self.tag])
        @inject
        async def get_role_by_id(role_id: int, session: AsyncSession = Depends(get_session)) -> SRoleInDB:
            controller = RoleController(session = session)
            result = await controller.get_by_id(role_id)
            if not result:
                raise HTTPException(status_code=404, detail="Role not found")
            return result

        @self.router.post('/roles/', status_code=status.HTTP_201_CREATED, tags=[self.tag])
        @inject
        async def create_role(data: SRole, session: AsyncSession = Depends(get_session)) -> dict:
            controller = RoleController(session = session)
            return await controller.create_role(data)
        
        @self.router.post('/roles/{role_id}', status_code=status.HTTP_201_CREATED, tags=[self.tag])
        @inject
        async def update_role(role_id: int, data: SRole,session: AsyncSession = Depends(get_session)) -> dict:
            controller = RoleController(session = session)
            return await controller.update_role(role_id, data)
        
        @self.router.delete('/roles/{role_id}', tags=[self.tag])
        @inject
        async def delete_role_by_id(role_id: int, session: AsyncSession = Depends(get_session)) -> dict:
            controller = RoleController(session = session)
            return await controller.delete_by_id(role_id)
