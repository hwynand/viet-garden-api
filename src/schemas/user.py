from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Shared props received via API on update"""

    fullname: str | None
    email: EmailStr | None
    phone_number: str | None
    address: str | None
    is_admin: bool | None = False


class UserCreate(BaseModel):
    """Props received via API on create"""

    email: EmailStr
    password: str
    is_admin: bool
    fullname: str
    phone_number: str
    address: str


class UserUpdate(UserBase):
    """Props received via API on update"""

    password: str | None


class User(UserBase):
    """Properties to return via API"""

    id: int | None

    class Config:
        orm_mode = True
