from pymongo import MongoClient, ASCENDING
client = MongoClient('mongodb://root:example@localhost:27017/')
db = client.kira

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
    }
]
result = db.players.insert_many(players_data)

print(f"Collection names : {db.list_collection_names()}")
for player in db.players.find():
    print(player)

result = database.players.update_one({"_id": username}, { "$set" : {"hashed_password": get_password_hash(userIn.hashed_password)}} )
