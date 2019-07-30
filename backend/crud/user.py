from pymongo.database import Database

from core.security import get_password_hash, verify_password
from models.user import UserInDB, UserUpdate


def get(database: Database, username: str):
    result = database.players.find_one({"_id": username})
    if result is None:
        return None
    return UserInDB(**result)


def update(database: Database, username: str, userIn: UserUpdate):
    result = database.players.update_one({"_id": username}, { "$set" : {"hashed_password": get_password_hash(userIn.hashed_password)}} )
    if result.acknowledged:
        result = database.players.find_one({"_id": username})
    if result is None:
        return None
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
