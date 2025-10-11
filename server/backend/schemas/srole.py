import json
from typing import Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class SRole(BaseModel):
    name: str = Field(examples=["Admin"])
    description: Optional[str]= Field(None, min_length=1, max_length=100, examples=["Super cool role"])
    permission: dict[str, bool] = Field(None, examples=[{"pages.create": True,
    "pages.edit": True,
    "settings.edit": False,
    "admin.access": False}])
    
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    @field_validator('permission', mode='before', check_fields=False)
    def trandform_permission(cls, value: Any):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Неверный формат JSON для permission")
        return value


class SRoleInDB(SRole):
    id: int