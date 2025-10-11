from __future__ import annotations
from pydantic import BaseModel, ConfigDict



class SClinicInServiceOut(BaseModel):
    clinic: "SClinicsWithImages" = []
    price: float

    model_config = ConfigDict(from_attributes=True)

class SServicesInClinicOut(BaseModel):
    service: "SServices" = []
    price: float

    model_config = ConfigDict(from_attributes=True)
