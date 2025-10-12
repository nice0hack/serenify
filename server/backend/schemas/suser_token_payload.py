from pydantic import BaseModel, Field
from typing import List, Optional


class SUserTokenPayload(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя",
    )
    login: str = Field(
        ...,
        description="Уникальный идентификатор пользователя",
    )
    role: int = Field(...)
    doctor_id: int | None = Field()
    exp: Optional[int] = Field(
        None, description="Время истечения токена (Unix timestamp)"
    )
