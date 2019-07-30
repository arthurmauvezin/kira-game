from fastapi import Depends, APIRouter

from api.utils.security import get_current_active_user, get_current_active_superuser
from models.msg import Msg
from models.user import User

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/isadmin/", response_model=Msg)
async def test(current_user: User = Depends(get_current_active_superuser)):
    return {"msg": "You are admin"}


#@router.post("/", response_model=User)
#def create_user(
#    *,
#    user_in: UserCreate,
#    current_user: UserInDB = Depends(get_current_active_superuser),
#):
#    """
#    Create new user.
#    """
#    bucket = get_default_bucket()
#    user = crud.user.get(bucket, username=user_in.username)
#    if user:
#        raise HTTPException(
#            status_code=400,
#            detail="The user with this username already exists in the system.",
#        )
#    user = crud.user.upsert(bucket, user_in=user_in, persist_to=1)
#    if config.EMAILS_ENABLED and user_in.email:
#        send_new_account_email(
#            email_to=user_in.email, username=user_in.username, password=user_in.password
#        )
#    return user

