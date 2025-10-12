from typing import Dict, Optional
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from core.db import Base


class MentalityCalendarModel(Base):
    __tablename__ = "mentality_calendar"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    mentality: Mapped[Optional[Dict]] = mapped_column(JSONB, default={})

    users = relationship("UserModel" , back_populates="calendar")
