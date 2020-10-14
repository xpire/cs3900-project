from fastapi import APIRouter

from backend.src.apis.api_stocks.endpoints import data_ret, search

stock_api_router = APIRouter()
stock_api_router.include_router(data_ret.router, tags=["data retrieval"])
stock_api_router.include_router(search.router, prefix="/users", tags=["search functions"])
