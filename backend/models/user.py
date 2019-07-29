from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
    admin: bool = None


class UserInDB(User):
    hashed_password: str

