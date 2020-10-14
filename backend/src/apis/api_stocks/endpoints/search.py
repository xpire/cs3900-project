from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from backend.src import crud, models, schemas
# from backend.src.api import deps
# from backend.src.core import security
# from backend.src.core.config import settings
# from backend.src.core.security import get_password_hash
# from backend.src.utils import (
#     generate_password_reset_token,
#     send_reset_password_email,
#     verify_password_reset_token,
# )

router = APIRouter()

# Start implementation here, this file handles searching

