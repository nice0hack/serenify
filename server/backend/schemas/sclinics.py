from schemas.sdoctros import SDoctorsInDB
from schemas.sservices_clinics import SServicesInClinicOut
from schemas.sfile_link import FileLinkOut
from pydantic import BaseModel, Field, ConfigDict

class SClinics(BaseModel):
    name: str = Field(example="HealthFirst Clinic")
    address: str = Field(example="123 Health St.")
    phone_number: str = Field(example="+1 (555) 123-4567")
    email: str = Field(example="info@healthfirst.com")
    description: str = Field(example="A clinic dedicated to providing the best health care.")
    coordinates: str = Field(example="37.7749,122.4194")

    model_config = ConfigDict(from_attributes=True)


class SClinicsWithImages(SClinics):
    id: int
    distance: float | None = None
    images: list["FileLinkOut"] = []
    

class SClinicsInDB(SClinicsWithImages):
    doctors: list["SDoctorsInDB"] = []
    services: list["SServicesInClinicOut"] = []
    