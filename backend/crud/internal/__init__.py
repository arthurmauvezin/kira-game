from crud.internal.user import InternalCrudUser
from utils import Singleton


class InternalCrud(metaclass=Singleton):

    def __init__(self):
        self.database = 'internal'
        self.user = InternalCrudUser()
