import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from core.config import config
from db.database import get_default_db
from models.token import TokenPayload
from models.user import UserInDB

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=config['JWT']['TOKEN_PATH'],
    scopes={
        "me": "Read informations about the current user.",
        "items": "Read items.",
        "user:read": "Read user data",
        "user:write": "Write user data",
        "room:read": "Read rooms data",
        "room:write": "Write rooms data",
        "system:read": "Read system data",
        "system:write": "Write system data"
    }
)


async def get_current_user(security_scopes: SecurityScopes, token: str = Security(reusable_oauth2)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )
    scope_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value}
    )

    try:
        payload = jwt.decode(token, config['JWT']['SECRET_KEY'], algorithms=[config['JWT']['ALGORITHM']])
        token_data = TokenPayload(**payload)
        username = token_data.sub.split(':')[1]
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    db = get_default_db()
    user = db.user.get(username=username)

    if not user:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise scope_exception
    return user


async def get_current_active_user(current_user: UserInDB = Security(get_current_user, scopes=["me"])):
    db = get_default_db()
    if not db.user.is_active(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: UserInDB = Security(get_current_user)):
    db = get_default_db()
    if not db.user.is_superuser(current_user):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
