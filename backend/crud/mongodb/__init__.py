from crud.mongodb.user import MongoCrudUser
from pymongo import MongoClient
from urllib.parse import quote_plus
from utils import Singleton


class MongoCrud(metaclass=Singleton):

    def __init__(self, username, password, server, database):
        uri = "mongodb://%s:%s@%s" % (
            quote_plus(username),
            quote_plus(password),
            server
        )
        client = MongoClient(uri)
        self.database = client[database]
        self.user = MongoCrudUser(self.database)
