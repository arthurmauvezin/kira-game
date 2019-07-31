from pymongo import MongoClient
from urllib.parse import quote_plus

from core.config import config


def get_default_db():
    uri = "mongodb://%s:%s@%s" % (
        quote_plus(config['MONGO']['USERNAME']), 
        quote_plus(config['MONGO']['PASSWORD']), 
        config['MONGO']['SERVER']
    )
    client = MongoClient(uri)
    db = client[config['MONGO']['DATABASE']]
    return db
