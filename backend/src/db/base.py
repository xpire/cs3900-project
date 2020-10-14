# Import all the models, so that Base has them before being
# imported by Alembic
from backend.src.db.base_class import Base  # noqa
from backend.src.models.stock import Stock  # noqa
from backend.src.models.stock_data import StockData
from backend.src.models.user import User  # noqa
