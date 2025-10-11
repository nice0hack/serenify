from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
# pyright: reportCallIssue=false


class SUser(BaseModel):
    login: str = Field(example="Login")
    email: EmailStr = Field(example="test@gmail.com")
    name: Optional[str] = Field(None, min_length=1, max_length=20, example="John Doe")
    role_id: int = Field(example=1)

    model_config = ConfigDict(from_attributes=True)


class SUserRegister(BaseModel):
    login: str = Field(example="Login")
    name: Optional[str] = Field(None, min_length=1, max_length=20, example="John Doe")
    email: EmailStr = Field(example="test@gmail.com")
    password: str = Field(example="password")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class SUserCreate(SUser):
    password: str = Field(example="password")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class SUserOut(SUser):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SUserDB(SUser):
    id: int
    password: str = Field(example="password")

    model_config = ConfigDict(from_attributes=True)


class SUserAuth(BaseModel):
    login: str = Field(example="Login")
    password: str = Field(example="password")

    model_config = ConfigDict(from_attributes=True)
