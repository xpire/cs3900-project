from backend.src.models.stock import Stock
from backend.src.crud.crud_stock import stock
from backend.src.db.session import SessionLocal

print(stock.get_stock_by_symbol())