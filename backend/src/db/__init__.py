# Import all the models, so that Base has them before being
# imported by Alembic
from src.db.base_model import BaseModel  # noqa
from src.models.notification import Notification
from src.models.stock import Stock  # noqa
from src.models.time_series import TimeSeries
from src.models.user import User  # noqa
