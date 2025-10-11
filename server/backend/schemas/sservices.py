# schemas/sservices.py
from schemas.sservices_clinics import SClinicInServiceOut
from pydantic import BaseModel, Field, ConfigDict

class SServices(BaseModel):
    name: str = Field(example="General Consultation")
    description: str = Field(example="A comprehensive health check-up and consultation.")
    duration_minutes: str = Field(example="30")

    model_config = ConfigDict(from_attributes=True)


class SServicesInDB(SServices):
    id: int
    clinics: list[SClinicInServiceOut] = []  # тоже строка

class SServicesCreate(SServices):
    clinics: list[dict] = Field(example=[{"id": 1, "price": 100.0}, {"id": 2, "price": 150.0}])