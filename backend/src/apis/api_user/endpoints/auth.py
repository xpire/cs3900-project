from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import from crud, model, etc..

router = APIRouter()

# Start implementation here, this file handles authentication

