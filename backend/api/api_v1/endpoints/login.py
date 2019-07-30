from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm

from api.utils.security import get_current_user, get_current_active_user, get_current_active_superuser
from core.config import config
from core.jwt import create_access_token
from db.database import get_default_db
from models.msg import Msg
from models.token import Token
from models.user import User, UserInDB, UserUpdate
from utils import generate_password_reset_token, send_reset_password_email, verify_password_reset_token

import crud

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    db = get_default_db()
    user = crud.user.authenticate(db, username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=int(config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES']))

    return {
        "access_token": create_access_token(
            data={"username": user.username}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/test-token", response_model=User)
def test_token(current_user: UserInDB = Depends(get_current_user)):
    """
    Test access token.
    """
    return current_user


@router.post("/password-recovery/{username}", response_model=Msg)
def recover_password(username: str):
    """
    Password Recovery.
    """
    db = get_default_db()
    user = crud.user.get(db, username=username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(username=username)
    send_reset_password_email(
        email_to=user.email, username=username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=Msg)
def reset_password(token: str = Body(...), new_password: str = Body(...)):
    """ 
    Reset password.
    """ 
    username = verify_password_reset_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")
    db = get_default_db()
    user = crud.user.get(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in = UserUpdate(username=username, hashed_password=new_password)
    user = crud.user.update(database=db, username=username, userIn=user_in)
    return {"msg": "Password updated successfully"}
