from pymongo.database import Database

from core.security import verify_password
from models.user import UserInDB


def get(database: Database, username: str):
    result = database.players.find_one({"_id": username})
    return UserInDB(**result)


def authenticate(database: Database, *, username: str, password: str):
    user = get(database, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: UserInDB):
    return not user.disabled

def is_superuser(user: UserInDB):
    return user.admin
