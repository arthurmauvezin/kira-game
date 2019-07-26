from datetime import datetime, timedelta

from fastapi import Depends, APIRouter
from passlib.context import CryptContext
from api.utils.security import get_current_active_user
from models.user import User 

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]