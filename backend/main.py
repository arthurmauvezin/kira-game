from fastapi import FastAPI
from api.api_v1.api import api_router
from core.config import config


app = FastAPI(title=config['APP']['TITLE'], openapi_url="/api/v1/openapi.json")

app.include_router(api_router, prefix="/api/v1")
