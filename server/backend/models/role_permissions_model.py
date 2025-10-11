from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db import Base

class RolePermissionModel(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)

    role = relationship("RoleModel", back_populates="role_permissions")
    permission = relationship("PermissionModel", back_populates="role_permissions")
