from abc import ABC, abstractmethod
from models.user import UserInDB, UserUpdate


class AbstractCrudUser(ABC):
    @abstractmethod
    def get(self, username: str):
        pass

    @abstractmethod
    def update(self, username: str, userIn: UserUpdate):
        pass

    @abstractmethod
    def authenticate(self, *, username: str, password: str):
        pass

    @abstractmethod
    def is_active(self, user: UserInDB):
        pass

    @abstractmethod
    def is_superuser(self, user: UserInDB):
        pass
