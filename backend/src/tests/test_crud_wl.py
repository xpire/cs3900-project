from datetime import datetime as dt

from pydantic import ValidationError
from src.core.utilities import log_msg
from src.crud.crud_user import user
from src.db.session import SessionLocal
# from src.models.time_series import TimeSeries
from src.schemas.time_series import TimeSeriesCreate

# INSERT INTO user (uid, email, username, balance, exp, level) values (1, 'admin@admin.com', 'admin', 10000, 0, 1)
ins = SessionLocal()
t_u = user.get_user_by_uid(ins, uid="1")


# user.create_order(db=ins, user_in=t_u, trade_type='buy', symbol="AAPL", quantity=50, limit=0.56)

user.delete_order(db=ins, user_in=t_u, identity=1)

for i in t_u.limit_orders:
    print(i.__dict__)
