from fastapi import Depends, APIRouter, Security
from api.utils.security import get_current_active_user, get_current_active_superuser
from models.room import Room
from models.user import User
from models.msg import Msg
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Room])
async def get_all_rooms(current_user: User = Security(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Security(get_current_active_user, scopes=["items"])):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/isadmin/", response_model=Msg)
async def test(current_user: User = Depends(get_current_active_superuser)):
    return {"msg": "You are admin"}
