from src.crud.crud_user import user
from src.db.session import SessionLocal

# INSERT INTO user (uid, email, username, balance, exp, level) values (1, 'admin@admin.com', 'admin', 10000, 0, 1)
ins = SessionLocal()
t_u = user.get_user_by_uid(ins, uid="1")


# add normal multiple
# t_u = user.add_to_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="AAPL",
#     p_amount=3,
#     price=83,
# )

# t_u = user.add_to_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="CBA",
#     p_amount=3,
#     price=43,
# )


# Trying compactification and average updating
# t_u = user.add_to_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="AAPL",
#     p_amount=5,
#     price=83,
# )

# t_u = user.add_to_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="AAPL",
#     p_amount=6,
#     price=70,
# )

# Normal dedcuct
# t_u = user.deduct_from_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="AAPL",
#     p_amount=6,
# )

# # Deduct non-existent
# t_u = user.deduct_from_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="IOO",
#     p_amount=7,
# )

# # Deduct till 0
# t_u = user.deduct_from_portfolio(
#     db=ins,
#     user_in=t_u,
#     p_symbol="AAPL",
#     p_amount=8,
# )