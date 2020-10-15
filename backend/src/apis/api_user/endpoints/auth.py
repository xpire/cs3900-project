from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import firebase_admin
from firebase_admin import auth, credentials

# Import from crud, model, etc..

router = APIRouter()

cred = credentials.Certificate("ecksdee-firebase.json")
firebase_admin.initialize_app(cred)

# Start implementation here, this file handles authentication


@router.get("/check")
async def get_user(id_token: str = Header(None)):

    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token["uid"]

    return uid
