from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func
from core.db import Base

class JWTKeyModel(Base):
    __tablename__ = "jwt_keys"
    kid: Mapped[str] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column()
    public_key: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[DateTime] =  mapped_column(DateTime(), server_default=func.now())