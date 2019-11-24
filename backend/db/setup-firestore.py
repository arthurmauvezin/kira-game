from google.cloud import firestore
from google.api_core.exceptions import NotFound
import datetime
# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DocumentAlreadyExistsError(Error):
    """Exception raised when trying to insert a document with an idea already existing in database

    Attributes:
        collection -- input collection in which document should have been created
        doc_id -- document id to insert in database
        message -- explanation of the error
    """

    def __init__(self, collection, doc_id):
        self.collection = collection
        self.doc_id = doc_id
        self.message = 'Document already exists and cannot be overriden'

class DocumentWasNotFoundError(Error):
    """Exception raised when trying to modify a document which does not exist

    Attributes:
        collection -- input collection in which document should have been created
        doc_id -- document id to insert in database
        message -- explanation of the error
    """

    def __init__(self, collection, doc_id):
        self.collection = collection
        self.doc_id = doc_id
        self.message = 'Document was not found'

def delete_collection(coll_ref, batch_size):
    """Delete all document from a collection

    Attributes:
        coll_ref -- collection reference. Ex: db.collection("mycollection")
        batch_size -- number of doc to delete on each batch
    """
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def create_game(game_id, title, description, default_settings):
    """Create a new type of game

    Attributes:
        game_id -- Id of the game document
        title -- Game title
        description -- Full description of the game
        default_settings -- Json parameters for the game
    """
    game_id = game_id.lower()
    doc = db.collection("games").document(game_id).get()

    if doc.exists:
        raise DocumentAlreadyExistsError("games", game_id)
    else:
        db.collection("games").document(game_id).set({
            "title": title,
            "description": description,
            "default_settings": default_settings,
            "active": True
        })

def create_user(user_id, connection_id, description):
    """Create a new user

    Attributes:
        user_id -- Id of the user document
        connection_id -- Firebase auth token id
        description -- Full description of the user
    """
    user_id = user_id.lower()
    doc = db.collection("users").document(user_id).get()

    if doc.exists:
        raise DocumentAlreadyExistsError("users", user_id)
    else:
        db.collection("users").document(user_id).set({
            "connection_id": connection_id,
            "description": description,
            "badges": ["newcomer"],
            "photo": None,
            "active": True
        })
        db.collection("users_rooms").document(user_id).set({
            "rooms": []
        })

def create_room(room_id, name, game_id, settings, status):
    """Create a new room

    Attributes:
        room_id -- Id of the room document
        name -- Name of the room
        game_id -- The type of game from Game class
        settings -- settings of the game played in the room
        status -- status of the game played in the room
    """
    room_id = room_id.lower()
    game_id = game_id.lower()
    doc = db.collection("rooms").document(room_id).get()

    if doc.exists:
        raise DocumentAlreadyExistsError("rooms", room_id)
    else:
        db.collection("rooms").document(room_id).set({
            "name": name,
            "game_id": db.collection('games').document(game_id),
            "settings": settings,
            "status": status,
            "active": True
        })
        db.collection("rooms_users").document(room_id).set({
            "users": []
        })

def add_players_to_room(room_id, users_ids, admin_rights=False):
    """Add one or many players to a room

    Attributes:
        room_id -- Id of the room document
        users_ids -- Array of user id
        admin_rights -- Wether or not added users should have admin rights
    """
    room_id = room_id.lower()
    doc = db.collection("rooms").document(room_id).get()

    if not doc.exists:
        raise DocumentWasNotFoundError("rooms", room_id)

    try:
        batch = db.batch()
        users_ids_ref = []
        for user_id in users_ids:
            user_id = user_id.lower()

            room_ref=db.collection("rooms").document(room_id)
            batch.update(db.collection("users_rooms").document(user_id), {
                "rooms": firestore.ArrayUnion([room_ref])
            })
            users_ids_ref.append(db.collection("users").document(user_id))

        if admin_rights:
            batch.update(db.collection("rooms_users").document(room_id), {
                "users": firestore.ArrayRemove(users_ids_ref),
                "admin": firestore.ArrayUnion(users_ids_ref)
            })
        else:
            batch.update(db.collection("rooms_users").document(room_id), {
                "users": firestore.ArrayUnion(users_ids_ref)
            })

        batch.commit()
    except NotFound as ex:
        raise ValueError("At least one of the player was not found")

def remove_players_from_room(room_id, users_ids):
    """Remove one or many players from a room

    Attributes:
        room_id -- Id of the room document
        users_ids -- Array of user id
    """
    room_id = room_id.lower()
    doc = db.collection("rooms").document(room_id).get()

    if not doc.exists:
        raise DocumentWasNotFoundError("rooms", room_id)

    try:
        batch = db.batch()
        users_ids_ref = []
        for user_id in users_ids:
            user_id = user_id.lower()

            room_ref=db.collection("rooms").document(room_id)
            batch.update(db.collection("users_rooms").document(user_id), {
                "rooms": firestore.ArrayRemove([room_ref])
            })
            users_ids_ref.append(db.collection("users").document(user_id))

        batch.update(db.collection("rooms_users").document(room_id), {
            "users": firestore.ArrayRemove(users_ids_ref),
            "admin": firestore.ArrayRemove(users_ids_ref)
        })
        batch.commit()
    except NotFound as ex:
        raise ValueError("At least one of the player was not found")

def get_users_rooms(user_id):
    """Get rooms from a user

    Attributes:
        user_id -- The user id to get rooms from
    """
    user_id = user_id.lower()
    doc = db.collection("users_rooms").document(user_id).get()

    if not doc.exists:
        raise DocumentWasNotFoundError("users_rooms", user_id)
    else:
        rooms_ref = doc.to_dict()['rooms']
        # Could be improved as we pass two times in for each loop
        rooms = [room.get().to_dict() for room in rooms_ref]
        for room in rooms:
            room['game_id'] = room['game_id'].get().to_dict()
        return rooms

def get_rooms_users(room_id):
    """Get users from a room

    Attributes:
        room_id -- The room id to get users from
    """
    room_id = room_id.lower()
    doc = db.collection("rooms_users").document(room_id).get()

    if not doc.exists:
        raise DocumentWasNotFoundError("rooms_userss", room_id)
    else:
        users_ref = doc.to_dict()
        users = [{user.id: user.get().to_dict()} for user in users_ref['users']]
        admins = [{user.id: user.get().to_dict()} for user in users_ref['admin']]
        return {"admin": admins, "user": users}

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
    delete_collection(db.collection("rooms_users"), 10)
    delete_collection(db.collection("users_rooms"), 10)

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
    create_user("boulbi", "fj02jfn2", "Team foutre")

    create_room("9fu32j", "The Origin", "tournament", tournament_settings, "not_started")
    create_room("f920fj", "The original killer", "killer", "killer_settings", "not_started")

    add_players_to_room("9fu32j", ["joffrey", "arthyshows", "clarita", "mae", "zenzoop"])
    remove_players_from_room("9fu32j", ["mae", "zenzoop"])
    add_players_to_room("f920fj", ["joffrey", "arthyshows", "clarita", "mae", "zenzoop", "gilbert", "willipiti"])
    remove_players_from_room("9fu32j", ["arthyshows"])
    add_players_to_room("9fu32j", ["arthyshows"])
    add_players_to_room("9fu32j", ["arthyshows"], admin_rights=True)

def get_informations():
    input_user = "arthyshows"
    print(f"{input_user}'s rooms:")
    for room in get_users_rooms(input_user):
        print(f"- {room}")

    input_room = "9fu32j"
    print(f"{input_room}'s users:")
    for user in get_rooms_users(input_room)['user']:
        print(f"- {user}")
    print(f"{input_room}'s admins:")
    for user in get_rooms_users(input_room)['admin']:
        print(f"- {user}")

def raise_exception():
    create_user("arthyshows", "32j4klf9", "The creator")
    create_room("9fu32j", "The Origin", "tournament", tournament_settings, "not_started")
    add_players_to_room("01f920fj", ["joffrey", "arthyshows", "clarita", "mae", "zenzoop", "gilbert", "willipiti"])
    add_players_to_room("9fu32j", ["gaston"])
    remove_players_from_room("9fu32j", ["mdsae", "zfdjsenzoop"])

#reset_database()
#get_informations()
try:
    remove_players_from_room("9fu32j", ["mdsae", "zfdjsenzoop"])
except (DocumentAlreadyExistsError, DocumentWasNotFoundError) as ex:
    print(ex.message)
    print(ex.args)

