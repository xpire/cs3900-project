from src.crud.crud_user import user
from src.db.session import SessionLocal

# INSERT INTO user (uid, email, username, balance, exp, level) values (1, 'admin@admin.com', 'admin', 10000, 0, 1)
ins = SessionLocal()
t_u = user.get_user_by_uid(ins, uid="1")

# # Normaladd
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