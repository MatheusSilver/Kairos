from fastapi import APIRouter

from app.core.config import settings
from app.routers import auth, users, utils

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(utils.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(auth.router)
