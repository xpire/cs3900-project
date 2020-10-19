from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import decode_token, get_current_user, get_db

router = APIRouter()

# TODO:
# - change to post again
# - current doesn't check whether the email matches the user's uid
@router.get("/create")
async def create_user(
    *,
    id_token: str = Header(None),
    email: str,
    db: Session = Depends(get_db),
) -> schemas.user:

    uuid = decode_token(id_token)
    user = crud.user.get_user_by_token(db, uuid=uuid)

    if not user:
        user = crud.user.create(db, obj_in=dict(email=email, uuid=uuid, username=email, balance=10000))

    # TODO raise error if already created

    return user


@router.get("/balance")
async def get_user_balance(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)) -> float:
    return user.balance


# @router.post("", status_code=201)
# async def create_user(
#     db=Depends(get_db),
#     id_token: str = Header(None),
#     username: str = Query(None),
#     email: str = Query(None),
# ):
#     uid = decode_token(id_token)
#     return {
#         "username": username,
#         "email": email,
#         "uid": uid,
#     }
