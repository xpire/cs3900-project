from fastapi import APIRouter

from backend.src.apis.api_stocks.endpoints import stocks

stock_api_router = APIRouter()
stock_api_router.include_router(stocks.router, tags=["stocks"])
