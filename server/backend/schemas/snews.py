from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from schemas import FileLinkOut

class SNewsBase(BaseModel):
    title: str = Field(..., max_length=300)
    html_text: str = Field(..., description="Валидный HTML (хранится как строка)")

class SNewsCreate(SNewsBase):
    pass


class SNewsOut(SNewsBase):
    id: int
    images: list[FileLinkOut] = []


    model_config = ConfigDict(from_attributes=True)
