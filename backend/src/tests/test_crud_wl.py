from datetime import datetime as dt

from pydantic import ValidationError
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.session import SessionLocal

# from src.models.time_series import TimeSeries
from src.schemas.time_series import TimeSeriesCreate
from src.schemas.transaction import TradeType

# INSERT INTO user (uid, email, username, balance, exp, level, resets) values (1, 'admin@admin.com', 'admin', 10000, 0, 1, 0)
ins = SessionLocal()
t_u = user.get_user_by_uid(db=ins, uid="1")


# user.create_order(db=ins, user_in=t_u, trade_type='buy', symbol="AAPL", quantity=50, limit=0.56)
# user.add_rec_to_hist_trans(db=ins, user_in=t_u, price_in=3.45, trade_type_in=TradeType.BUY, amount_in=34, symbol_in="AAPL")
# user.add_rec_to_hist_trans(db=ins, user_in=t_u, price_in=6.75, trade_type_in=TradeType.SELL, amount_in=20, symbol_in="CBA")

# for x in t_u.transaction_hist: print(x.__dict__)
