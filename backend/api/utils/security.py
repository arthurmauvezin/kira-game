import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

import crud
from core.config import config
from db.database import get_default_db
from models.token import TokenPayload
from models.user import UserInDB

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=config['JWT']['TOKEN_PATH'])


async def get_current_user(token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, config['JWT']['SECRET_KEY'], algorithms=[config['JWT']['ALGORITHM']])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    db = get_default_db()
    user = crud.user.get(db, username=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
