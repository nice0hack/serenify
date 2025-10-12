import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from core.db import Base


class AppointmentsModel(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"), nullable=True
    )
    services_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(nullable=True)
    end_time: Mapped[datetime.time] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="booked", nullable=False
    )  # CHECK (status IN ('booked', 'cancelled', 'completed'))

    doctors = relationship("DoctorsModel", back_populates="appointments")
    services = relationship("ServicesModel", back_populates="appointments")
    users = relationship("UserModel", back_populates="appointments")
