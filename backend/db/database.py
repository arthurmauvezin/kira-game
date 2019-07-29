from pymongo import MongoClient, ASCENDING

from core.config import config

def get_default_db():
    client = MongoClient('mongodb://'+config['MONGO']['USERNAME']+':'+config['MONGO']['PASSWORD']+'@'+config['MONGO']['SERVER']+':'+config['MONGO']['PORT']+'/')
    db = client[config['MONGO']['DATABASE']]

    return db
