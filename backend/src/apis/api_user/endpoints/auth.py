from datetime import timedelta
from typing import Any

from backend.src.core.auth import decode_token
from backend.src.db.session import get_db
from backend.src.models import User
from backend.src import schemas
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from backend.src.crud.crud_user import user as crud_user

# Import from crud, model, etc..

router = APIRouter()

# Start implementation here, this file handles authentication




@router.get("/create")
async def create_user(
    *,
    id_token: str = Header(None),
    email: str,
    db: Session = Depends(get_db),
):
    uuid = decode_token(id_token)
    user = crud_user.get_user_by_token(db, uuid=uuid)

    if not user:
        user = crud_user.create(db, obj_in=dict(email=email, uuid=uuid, username="ian", balance=10000))
    return user

@router.get("/balance")
async def get_user_balance(id_token: str = Header(None), db: Session = Depends(get_db)):
    uuid = decode_token(id_token)
    user = crud_user.get_user_by_token(db, uuid=uuid)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="no user exists",
        )
    
    return user.balance


# @router.get("")
# async def get_user(id_token: str = Header(None)):

#     return decode_token(id_token)


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

# TODO THIS VERY BAD, refer to deps in cookie
# @router.post("/", response_model=schemas.User)
# def create_user(
#     *,
#     db: Session = Depends(get_db),
#     user_in: schemas.UserCreate,
#     id_token: str = Header(None)
# ) -> Any:
#     """
#     Create new user.
#     """
#     user = crud.user.get_user_by_token(db, uuid=id_token)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system.",
#         )

#     user = crud_user.create(db, obj_in=user_in)
#     return user
