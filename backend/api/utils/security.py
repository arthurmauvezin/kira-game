import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

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
        print(payload)
        print(token_data)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    db = get_default_db()
    user = crud.user.get(db, username=token_data.sub.split(':')[1])
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_active_user(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
