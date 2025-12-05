from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr = Field(..., description="Email address of user")
    fullname: str = Field(..., description="username of user")


class UserBase(User):
    pass


class UserCreate(UserBase):
    sid: UUID = Field(..., description="SID of user")
    first_name: str = Field(..., description="First name of user")
    last_name: str = Field(..., description="Last name of user")
    middle_name: str = Field(..., description="Middle name of user")
    hashed_password: str = Field(..., description="Hashed password of user")
    confirm_hashed_password: str = Field(..., description="Confirm hashed password of user")
    created_at: datetime = Field(..., description="User created at")
    updated_at: datetime = Field(..., description="User updated at")


class UserUpdate(BaseModel):
    last_name: str = Field(..., description="Last name of user")
    first_name: str = Field(..., description="First name of user")
    middle_name: str = Field(..., description="Middle name of user")
    updated_at: datetime = Field(..., description="User updated at")


class UserUpdatePass(BaseModel):
    hashed_password: str = Field(..., description="Hashed password of user")
    confirm_hashed_password: str = Field(..., description="Confirm hashed password of user")

