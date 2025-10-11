from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class ServicesModel(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration_minutes: Mapped[str] = mapped_column(nullable=True)
    images = relationship(
        "FileLinkModel",
        primaryjoin="and_(foreign(FileLinkModel.linked_id) == cast(ServicesModel.id, String), "
        "FileLinkModel.linked_type == 'services')",
        lazy="selectin",
        cascade="all, delete",
        backref="service_owner",
    )

    clinics = relationship("ServicesClinicsModel", back_populates="service")
    appointments = relationship(
        "AppointmentsModel",
        back_populates="services",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
