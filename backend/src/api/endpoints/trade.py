import json
import os
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud
from src.api.deps import get_db
from src.core.config import settings
from src.real_time_market_data.data_provider import (
    CompositeDataProvider,
    LatestClosingPriceProvider,
    RealTimeDataProvider,
    SimulatedDataProvider,
    SimulatedStock,
)
from twelvedata import TDClient

API_URL = "https://api.twelvedata.com"
API_KEY = settings.TD_API_KEY

router = APIRouter()
