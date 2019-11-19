from core.security import get_password_hash, verify_password
from crud.user import AbstractCrudUser
from models.user import UserInDB, UserUpdate


class MongoCrudUser(AbstractCrudUser):

    def __init__(self, database):
        self.database = database

    def get(self, username: str):
        result = self.database.players.find_one({"_id": username})
        if result is None:
            return None
        return UserInDB(**result)

    def update(self, username: str, userIn: UserUpdate):
        result = self.database.players.update_one(
            {"_id": username},
            {"$set": {"hashed_password": get_password_hash(userIn.hashed_password)}}
        )
        if result.acknowledged:
            result = self.database.players.find_one({"_id": username})
        if result is None:
            return None
        return UserInDB(**result)

    def authenticate(self, *, username: str, password: str):
        user = self.get(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserInDB):
        return not user.disabled

    def is_superuser(self, user: UserInDB):
        return user.admin
