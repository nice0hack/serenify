from typing import Any, Dict
from sqlalchemy import JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    role_permissions = relationship(
        "RolePermissionModel", back_populates="role", cascade="all, delete-orphan"
    )
    permissions = relationship(
        "PermissionModel", secondary="role_permissions", viewonly=True
    )

    users = relationship("UserModel", back_populates="role")
