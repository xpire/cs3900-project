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

# Normaladd
# u_t_u = user.add_to_watch_list(db=ins, user_in=t_u, w_symbol="CBA")
# u_t_u = user.add_to_watch_list(db=ins, user_in=t_u, w_symbol="AAPL")


# for x in t_u.watchlist:
#     print(x.stock.__dict__)


# # Trying to add something that doesnt exist
# u_t_u = user.add_to_watch_list(db=ins, user_in=t_u, w_symbol="DOESNT_EXIST")


# Normal delete
# u_t_u = user.delete_from_watch_list(db=ins, user_in=t_u, w_symbol="AAPL")
# u_t_u = user.delete_from_watch_list(db=ins, user_in=t_u, w_symbol="CBA")

# Trying to delete valid symbol that doesnt exist in watchlist
# u_t_u = user.delete_from_watch_list(db=ins, user_in=t_u, w_symbol="CAR")


# Deleting non-existent symbol
# u_t_u = user.delete_from_watch_list(db=ins, user_in=t_u, w_symbol="DOESNT_EXIST")

# print(u_t_u.__dict__)


# log_msg("Trying to delete a watchlist that doesn't exist.", "WARNING")


# ts = TimeSeries(
#     datetime=datetime.now(),
#     symbol="AAPL",
#     low=0.45,
#     high=6,
#     open_p=3.4,
#     close_p=9.7,
#     volume=3.56,
# )

# print(ts.__dict__)


try:
    ts = TimeSeriesCreate(
        datetime=dt.now(),
        symbol="AAP",
        low=0.45,
        high=6,
        open_p="something",
        close_p=9.7,
        volume=3.56,
    )
except ValidationError as e:
    log_msg(f"Type error inserting time series data.", "ERROR")

finally:
    print("return here")
