from pydantic import BaseModel
from typing import List
from models.user import User


class Room(BaseModel):
    code: str
    game_type: str = None
    players: List[User] = []
