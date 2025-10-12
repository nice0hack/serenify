import calendar
from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    login: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=True)

    role = relationship("RoleModel", back_populates="users")
    appointments = relationship("AppointmentsModel", back_populates="users")
    doctor = relationship("DoctorsModel", back_populates="users")
    calendar =relationship("MentalityCalendarModel", back_populates="users")
