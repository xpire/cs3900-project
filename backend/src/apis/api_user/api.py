from fastapi import APIRouter

from backend.src.apis.api_user.endpoints import auth, utils

user_api_router = APIRouter()
user_api_router.include_router(auth.router, tags=["auth"])
user_api_router.include_router(utils.router, prefix="/utils", tags=["utils"])