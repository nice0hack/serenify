from pydantic import BaseModel, ConfigDict
from schemas.simage import ImageOut

class FileLinkOut(BaseModel):
    id: int
    file_id: int
    image: ImageOut

    model_config = ConfigDict(from_attributes=True)

