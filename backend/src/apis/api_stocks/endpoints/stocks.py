from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()

# Start implementation here, this file handles batch and single stock data retrieval

@router.get("/symbols")
async def get_symbols():
    # For now, return hardcoded data
    return [{"symbol": "TLS", "exchange": "ASX"}, {"symbol": "SVW", "exchange": "ASX"}]