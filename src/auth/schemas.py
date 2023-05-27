import re
from datetime import datetime

from pydantic import EmailStr, validator, UUID4, Field, constr
from src.schemas import BaseModel
from typing import Optional


STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


def validate_password(password: str) -> str:
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise ValueError(
            "Password must contain at least "
            "one lower character, "
            "one upper character, "
            "digit or "
            "special symbol"
        )
    return password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class UserBase(BaseModel):
    username: constr(
        regex='^[a-zA-Z0-9_\-]+$',
        to_lower=True,
        strip_whitespace=True,
        min_length=3,
        max_length=16)
    email: EmailStr


class UserRead(UserBase):
    id: UUID4


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_validation(cls, password):
        return validate_password(password)


class UserUpdate(BaseModel):
    username: Optional[constr(
        regex='^[a-zA-Z0-9_\-]+$',
        to_lower=True,
        strip_whitespace=True,
        min_length=3,
        max_length=30)]
    email: Optional[EmailStr]
    password: Optional[str]

    @validator('password')
    def password_validation(cls, password):
        return validate_password(password)
