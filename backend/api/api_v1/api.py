from fastapi import APIRouter

from api.api_v1.endpoints import token, users

api_router = APIRouter()

api_router.include_router(token.router, tags=["token"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
