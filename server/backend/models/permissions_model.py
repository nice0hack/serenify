from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from core.db import Base

class PermissionModel(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)  # "pages.create"
    name: Mapped[str] = mapped_column()             # "Создание страниц" – для UI
    description: Mapped[str] = mapped_column(nullable=True)  # Доп. тех. описание

    role_permissions = relationship("RolePermissionModel", back_populates="permission", cascade="all, delete-orphan")
