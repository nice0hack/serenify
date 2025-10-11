from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ImageOut(BaseModel):
    id: int
    filename: str
    url: str
    alt: Optional[str]
    title: Optional[str]
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
