import re

from pydantic import EmailStr, validator, Field

from core.schemas import BaseModelSchema


class UserBaseSchema(BaseModelSchema):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8)

    @validator('password')
    def check_password(cls, password: str):
        if re.search('[0-9]', password) is None:
            raise ValueError("Make sure password contains a number")
        elif re.search('[A-Z]', password) is None:
            raise ValueError("Make sure password contains a capital letter")
        elif re.search('[@$!%*?&]', password) is None:
            raise ValueError("Password must contain at least one of these special characters: @$!%*?&")
        return password

    class Config:
        schema_extra = {
            "example": {
                "email": "user@cimer.com",
                "first_name": "FirstName",
                "last_name": "LastName",
                "password": "examplePassword123!",
            }
        }


class UserReadSchema(UserBaseSchema):
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModelSchema):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@cimer.com",
                "password": "examplePassword123!",
            }
        }
