# Import all the models, so that Base has them before being
# imported by Alembic
from src.db.base_model import BaseModel  # noqa
from src.models import *
