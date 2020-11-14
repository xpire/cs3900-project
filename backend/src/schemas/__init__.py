"""
Schemas
- Defines various types (i.e. schemas and enums) commonly used by the application
- Some schemas (suffixed APIout) define formats according to which data will be sent through the endpoints
- Some schemas (suffixed DBcreate) define acceptable formats for creating certain database table entries
- Some schemas are used as a baseclass for other shcemas, some are used for type conversion
- TradeType defines different trading options (e.g. buy, sell, short, cover)
- OrderType defines different order options (e.g. market, limit)
"""

from .combined import BasicDetail, NotificationAPIout, UserDetailAPIout
from .exchange import Exchange
from .net_worth_time_series import NetWorthTimeSeriesAPIout, NetWorthTimeSeriesBase
from .pending_order import LimitOrderDBcreate, MarketOrderDBcreate, PendingOrderAPIout, PendingOrderDBcreate
from .portfolio import PortfolioAPIout, PortfolioStatAPIout, PositionAPIout
from .stock import StockAPIout, StockRealTimeAPIout, TradingHoursInfo
from .time_series import TimeSeriesAPIout, TimeSeriesBase, TimeSeriesDBcreate
from .transaction import (
    ClosingTransaction,
    OpeningTransaction,
    OrderType,
    TradeType,
    TransactionAPIout,
    TransactionBase,
    TransactionDBcreate,
)
from .user import LeaderboardAPIout, LeaderboardUserWithUid, UserAPIout, UserCreate, UserDBout
