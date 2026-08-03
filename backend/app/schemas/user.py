import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    codpes: str = Field(unique=True, index=True, max_length=16)
    name: str = Field(max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    is_apoio: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    pass


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    is_apoio: bool | None = None


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
