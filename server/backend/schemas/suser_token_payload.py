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
    exp: Optional[int] = Field(
        None, description="Время истечения токена (Unix timestamp)"
    )
