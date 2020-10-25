from src.crud.crud_user import user
from src.db.session import SessionLocal

# INSERT INTO user (uid, email, username, balance, exp, level) values (1, 'admin@admin.com', 'admin', 10000, 0, 1)
ins = SessionLocal()
t_u = user.get_user_by_uid(db=ins, uid="1")


# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=12, price=67.3)


# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)
# user.add_transaction(db=ins, user_in=t_u, t_type="short", p_symbol="AAPL", p_amount=12, price=67.3)


# user.deduct_transaction(db=ins, user_in=t_u, t_type="long", p_symbol="AAPL", p_amount=24)
