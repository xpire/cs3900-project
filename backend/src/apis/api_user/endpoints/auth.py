from datetime import timedelta
from typing import Any

import firebase_admin
from backend.src.core.auth import decode_token
from backend.src.db.session import get_db
from backend.src.models import User
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session

# Import from crud, model, etc..

router = APIRouter()

# Start implementation here, this file handles authentication


@router.get("")
async def get_user(id_token: str = Header(None)):

    return decode_token(id_token)


@router.post("", status_code=201)
async def create_user(
    db=Depends(get_db),
    id_token: str = Header(None),
    username: str = Query(None),
    email: str = Query(None),
):
    uid = decode_token(id_token)
    return {
        "username": username,
        "email": email,
        "uid": uid,
    }
