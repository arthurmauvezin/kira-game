from configparser import SafeConfigParser
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

config = SafeConfigParser(os.environ)
config.read('config.ini')

uri = "mongodb://%s:%s@%s" % (
    quote_plus(config['MONGO']['USERNAME']),
    quote_plus(config['MONGO']['PASSWORD']),
    config['MONGO']['SERVER']

)
client = MongoClient(uri)
db = client[config['MONGO']['DATABASE']]

db.players.delete_many({})

players_data = [
    {
        "_id": "johndoe",
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "admin": True
    },
    {
        "_id": "player1",
        "username": "player1",
        "full_name": "Player one",
        "email": "player1@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "admin": False
    },
    {
        "_id": "player2",
        "username": "player2",
        "full_name": "Player two",
        "email": "player2@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "admin": False
    },
    {
        "_id": "player3",
        "username": "player3",
        "full_name": "Player three",
        "email": "player3@example.com",
        "hashed_password": "$2b$32$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "admin": False
    },
    {
        "_id": "amauvezin",
        "username": "amauvezin",
        "full_name": "Arthur Mauvezin",
        "email": "arthur.mauvezin@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "admin": True
    }
]
result = db.players.insert_many(players_data)

print(f"Collection names : {db.list_collection_names()}")
for player in db.players.find():
    print(player)

