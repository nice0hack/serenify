from pydantic import BaseModel


class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class STokenWithRefresh(SToken):
    refresh_token: str


class STokenRefresh(BaseModel):
    refresh_token: str
