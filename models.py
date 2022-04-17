from pydantic import validator, BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum
import re

# USER
class UserBase(BaseModel):
    id: UUID = uuid4()
    phone_number: str
    email: EmailStr
    name: str
    nickname: str

    @validator("phone_number")
    def validate_phone(cls, v):
        regex = re.compile('\d{3}-\d{3,4}-\d{4}')
        if not regex.match(str(v)):
            raise ValueError("Phone number is invalid")
        return v


class UserLoginType(str, Enum):
    phone_number = "phone_number"
    email = "email"
    nickname = "nickname"


class UserLogin(BaseModel):
    type: UserLoginType
    identification_info: str
    password: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    password: str
    hashed_password: str


# Phone Verification
class VerificationType(str, Enum):
    sign_up = "sign_up"
    find_password = "find_password"


class Verification(BaseModel):
    type: VerificationType
    phone_number: str
    @validator("phone_number")
    def validate_phone(cls, v):
        regex = re.compile('\d{3}-\d{3,4}-\d{4}')
        if not regex.match(str(v)):
            raise ValueError("Phone number is invalid")
        return v


class VerificationInDB(Verification):
    verification_code: int

