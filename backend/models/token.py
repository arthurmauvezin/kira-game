from pydantic import BaseModel
from typing import List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    iss: str = None
    scopes: List[str] = []
