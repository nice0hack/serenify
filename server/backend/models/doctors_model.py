from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class DoctorsModel(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    specialty: Mapped[str] = mapped_column(index=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinics.id"), nullable=False)

    clinics = relationship("ClinicsModel", back_populates="doctors")
    weekly_schedule = relationship(
        "WorkerWeeklyScheduleModel",
        back_populates="doctors",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    exceptions_schedule = relationship(
        "WorkerExceptionsSheduleModel",
        back_populates="doctors",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    appointments = relationship(
        "AppointmentsModel",
        back_populates="doctors",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    users = relationship("UserModel", back_populates="doctor", lazy="selectin")

    images = relationship(
        "FileLinkModel",
        primaryjoin="and_(foreign(FileLinkModel.linked_id) == cast(DoctorsModel.id, String), "
        "FileLinkModel.linked_type == 'doctors')",
        lazy="selectin",
        cascade="all, delete",
        backref="doctor_owner",
    )
