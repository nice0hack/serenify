from pydantic import BaseModel, ConfigDict, Field
from schemas.sfile_link import FileLinkOut

class SDoctors(BaseModel):
    id: int | None = None
    name: str = Field(example="Dr. John Doe")
    specialty: str = Field(example="Cardiology")
    phone_number: str = Field(example="+1234567890")
    email: str = Field(example="dr.johndoe@example.com")
    description: str = Field(example="Experienced cardiologist with over 10 years in practice.")
    clinic_id: int = Field(example=1)

    model_config = ConfigDict(extra="forbid", from_attributes=True)

class SDoctorsInDB(SDoctors):
    slots: list[dict] = []
    images: list[FileLinkOut] = []

    model_config = ConfigDict(from_attributes=True)


