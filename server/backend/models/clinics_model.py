from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class ClinicsModel(Base):
    __tablename__ = "clinics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(index=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    coordinates: Mapped[str] = mapped_column(String, nullable=True)

    doctors = relationship("DoctorsModel", back_populates="clinics")
    services = relationship("ServicesClinicsModel", back_populates="clinic")

    images = relationship(
        "FileLinkModel",
        primaryjoin="and_(foreign(FileLinkModel.linked_id) == cast(ClinicsModel.id, String), "
        "FileLinkModel.linked_type == 'clinics')",
        lazy="selectin",
        cascade="all, delete",
        backref="clinic_owner",
    )
