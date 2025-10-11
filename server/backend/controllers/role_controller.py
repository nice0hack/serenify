from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from schemas import SRole, SRoleInDB
from sqlalchemy.ext.asyncio import AsyncSession
from models import RoleModel, RolePermissionModel, PermissionModel
from controllers.base_controller import BaseController

class RoleController(BaseController[RoleModel, SRoleInDB]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RoleModel, SRoleInDB)

    async def get_by_id(self, role_id: int) -> SRoleInDB | None:
        role_model = await self.session.get(RoleModel, role_id)
        if not role_model:
            return None

        all_stmt = select(PermissionModel)
        all_result = await self.session.execute(all_stmt)
        all_permissions = all_result.scalars().all()
        all_codes = {perm.code for perm in all_permissions}

        stmt = (
            select(PermissionModel.code)
            .join(
                RolePermissionModel,
                PermissionModel.id == RolePermissionModel.permission_id,
            )
            .where(RolePermissionModel.role_id == role_id)
        )
        result = await self.session.execute(stmt)
        active_permissions = {code for code, in result.all()}

        permission_dict = {code: (code in active_permissions) for code in all_codes}

        return SRoleInDB(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description,
            permission=permission_dict,
        )
    
    async def get_all(self) -> list[SRoleInDB]:
        stmt = select(RoleModel).options(selectinload(RoleModel.permissions))
        result = await self.session.execute(stmt)
        roles = result.scalars().all()
        roles_list = []
        for role in roles:
            all_stmt = select(PermissionModel)
            all_result = await self.session.execute(all_stmt)
            all_permissions = all_result.scalars().all()
            all_codes = {perm.code for perm in all_permissions}       
           
            active_permissions = {perm.code for perm in role.permissions}

            permission_dict = {code: (code in active_permissions) for code in all_codes}

            roles_list.append(
                SRoleInDB(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    permission=permission_dict,
                )
            )
        return roles_list
        
    async def create_role(self, role: SRole):
        role_model = RoleModel(name=role.name, description=role.description)
        self.session.add(role_model)
        await self.session.flush() 

        enabled_permissions = [
            code for code, enabled in role.permission.items() if enabled
        ]

        if enabled_permissions:
            stmt = select(PermissionModel).where(
                PermissionModel.code.in_(enabled_permissions)
            )
            result = await self.session.execute(stmt)
            permission_objs = result.scalars().all()

            role_permissions = [
                RolePermissionModel(role_id=role_model.id, permission_id=perm.id)
                for perm in permission_objs
            ]
            self.session.add_all(role_permissions)

        await self.session.commit()
        return {"success": True, "msg": "Role created"}

    async def update_role(self, role_id: int, role: SRole):
        role_model = await self.session.get(RoleModel, role_id)
        if not role_model:
            return {"success": False, "msg": "Role not found"}

        role_model.name = role.name
        role_model.description = role.description

        await self.session.execute(
            delete(RolePermissionModel).where(RolePermissionModel.role_id == role_id)
        )

        enabled_permissions = [
            code for code, enabled in role.permission.items() if enabled
        ]

        if enabled_permissions:
            stmt = select(PermissionModel).where(
                PermissionModel.code.in_(enabled_permissions)
            )
            result = await self.session.execute(stmt)
            permission_objs = result.scalars().all()

            new_links = [
                RolePermissionModel(role_id=role_id, permission_id=perm.id)
                for perm in permission_objs
            ]
            self.session.add_all(new_links)

        await self.session.commit()
        return {"success": True, "msg": "Role updated"}
