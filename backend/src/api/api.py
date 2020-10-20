from fastapi import APIRouter
from src.api.endpoints import auth, stocks
from src.db import base_model_import_all as base_model
from src.db.session import engine

base_model.BaseModel.metadata.create_all(bind=engine)

api_router = APIRouter()
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])
