from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    admin: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UserUpdate(UserInDB):
    hashed_password: Optional[str] = None


class UserCreate(UserInDB):
    username: str
    password: str
    disabled: bool = False
    admin: bool = False


class UserNew(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None
    admin: Optional[bool] = None
