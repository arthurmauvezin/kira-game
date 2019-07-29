from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from core.config import config
from core.jwt import create_access_token
from db.database import get_default_db
from models.token import Token

import crud

router = APIRouter()


@router.post("/token", response_model=Token)
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
