from core.security import get_password_hash, verify_password
from crud.user import AbstractCrudUser
from models.user import UserInDB, UserUpdate


class InternalCrudUser(AbstractCrudUser):

    def __init__(self):
        self.db = {
            "dumb": {
                "username": "dumb",
                "email": "dumb.retarded@gmail.com",
                "full_name": "Dumb Retarded",
                "disabled": False,
                "admin": True,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            },
            "dumber": {
                "username": "dumber",
                "email": "dumber.retarded@gmail.com",
                "full_name": "Dumber Retarded",
                "disabled": False,
                "admin": False,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            }
        }

    def get(self, username: str):
        result = None
        if username in self.db:
            result = self.db[username]
        if result is None:
            return None
        return UserInDB(**result)

    def update(self, username: str, userIn: UserUpdate):
        self.db[username]["hashed_password"] = get_password_hash(userIn.hashed_password)
        result = self.db[username]
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
