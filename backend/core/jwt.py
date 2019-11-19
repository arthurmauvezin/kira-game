from core.config import config
from datetime import datetime, timedelta

import jwt


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"iss": config['JWT']['ISSUER']})
    encoded_jwt = jwt.encode(to_encode, config['JWT']['SECRET_KEY'], algorithm=config['JWT']['ALGORITHM'])
    return encoded_jwt
