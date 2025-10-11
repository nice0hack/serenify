from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.db import Base


class ServicesClinicsModel(Base):
    __tablename__ = "services_clinics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinics.id"), nullable=False)
    price: Mapped[int] = mapped_column(index=True, nullable=True)

    clinic = relationship("ClinicsModel", back_populates="services")
    service = relationship("ServicesModel", back_populates="clinics")
