from google.cloud import firestore
import datetime
# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def create_game(game_id, title, description, default_settings):
    doc_ref = db.collection("games").document(game_id.lower()).set({
        "title": title,
        "description": description,
        "default_settings": default_settings
    })

def create_user(username, connection_id, description):
    doc_ref = db.collection("users").document(username.lower()).set({
        "connection_id": connection_id,
        "description": description,
        "badges": ["newcomer"],
        "photo": "TBD"
    })
    doc_ref = db.collection("user_rooms").document(username.lower()).set({
        "rooms": []
    })

def create_room(room_id, name, game_type, settings, status):
    doc_ref = db.collection("rooms").document(room_id.lower()).set({
        "name": name,
        "game_type": db.collection('games').document(game_type.lower()),
        "settings": settings,
        "status": status
    })
    doc_ref = db.collection("room_users").document(room_id.lower()).set({
        "users": []
    })

def add_players_to_room(room_id, usernames):
    batch = db.batch()
    usernames_ref = [db.collection("users").document(user_ref) for user_ref in usernames]
    batch.update(db.collection("room_users").document(room_id.lower()), {
        "users": firestore.ArrayUnion(usernames_ref)
    })
    for username in usernames:
        room_ref=db.collection("rooms").document(room_id.lower())
        batch.update(db.collection("user_rooms").document(username.lower()), {
            "rooms": firestore.ArrayUnion([room_ref])
        })
    batch.commit()

def remove_players_from_room(room_id, usernames):
    batch = db.batch()
    usernames_ref = [db.collection("users").document(user_ref) for user_ref in usernames]
    batch.update(db.collection("room_users").document(room_id.lower()), {
        "users": firestore.ArrayRemove(usernames_ref)
    })
    for username in usernames:
        room_ref=db.collection("rooms").document(room_id.lower())
        batch.update(db.collection("user_rooms").document(username.lower()), {
            "rooms": firestore.ArrayRemove([room_ref])
        })
    batch.commit()

def get_user_rooms(username):
    doc_ref = db.collection("user_rooms").document(username.lower())
    rooms_ref = doc_ref.get().to_dict()['rooms']
    rooms = [room.get().to_dict() for room in rooms_ref]
    for room in rooms:
        room['game_type'] = room['game_type'].get().to_dict()
    return rooms

tournament_settings = {
        "bracket": True,
        "looser_bracket": False,
        "referee": True,
        "nb_contestors": 4,
        "started": False,
        "template_match": {
                "contenders": [
                        { "type": "username" },
                        { "type": "username" }
                ],
                "played": True,
                "referee": 2,
                "winner": [ 3 ],
                "looser": [ 4 ]
        }
}

def reset_database():
    delete_collection(db.collection("rooms"), 10)
    delete_collection(db.collection("users"), 10)
    delete_collection(db.collection("games"), 10)
    delete_collection(db.collection("room_users"), 10)
    delete_collection(db.collection("user_rooms"), 10)

    create_game("tournament", "Tournament", "Figth each other through rounds. Only the better will stand", tournament_settings)
    create_game("killer", "The Killer", "Kill each other in a fun way. Only one will stand", "killer_settings")

    create_user("arthyshows", "32j4klf9", "The creator")
    create_user("clarita", "93jf93hf", "The wife")
    create_user("gilbert", "f3j2cw0a", "Guada boy")
    create_user("floazul", "if9ds3n3", "boloss king")
    create_user("mae", "34j0fjds0", "Christophe")
    create_user("willipiti", "2htalpx0", "Chaton")
    create_user("zenzoop", "q1JUi94R", "Clemtouille")
    create_user("fifi", "yYYwyyEJ", "ROmain michel")
    create_user("annesuce", "o7FNTmYy", "Je serai un peu en retard")
    create_user("joffrey", "tAvixOba", "Remet nous des glaçon")
    create_user("Yanus", "e9lmU9NM", "Gossbo")
    create_user("Chachatte", "gkYhniBs", "Pince à linge girl")

    create_room("9fu32j", "The Origin", "tournament", tournament_settings, "not_started")
    create_room("f920fj", "The original killer", "killer", "killer_settings", "not_started")

    add_players_to_room("9fu32j", ["joffrey", "arthyshows", "clarita", "mae", "zenzoop"])
    remove_players_from_room("9fu32j", ["mae", "zenzoop"])
    add_players_to_room("f920fj", ["joffrey", "arthyshows", "clarita", "mae", "zenzoop", "gilbert", "willipiti"])

# reset_database()
for room in get_user_rooms("arthyshows"):
    print(room)

