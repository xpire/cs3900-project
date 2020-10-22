from typing import Any

from pydantic import BaseModel as BaseSchema


class Stats(BaseSchema):
    user: Any  # UserDM -> balance, portfolio (units owned, owed), watchlist, etc.
    short_worth: float
    long_worth: float
