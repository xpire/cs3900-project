from fastapi import APIRouter
from src.api.endpoints import auth, leaderboard, portfolio, stocks, trade, transactions, watchlist
from src.db import base_model_import_all as base_model
from src.db.session import engine

# base_model.BaseModel.metadata.create_all(bind=engine)

api_router = APIRouter()
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(trade.router, prefix="/trade", tags=["trade"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
