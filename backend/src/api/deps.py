from typing import Generator, Optional

from fastapi import Depends, Header, HTTPException
from firebase_admin import auth
from sqlalchemy.orm import Session
from src import crud, models
from src.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def decode_token(id_token: str):
    try:
        return auth.verify_id_token(id_token)["uid"]
    except Exception as e:
        raise HTTPException(401, detail="The authentication token is invalid.")


async def get_current_user(
    id_token: str = Header(None), db: Session = Depends(get_db)
) -> models.User:

    user = crud.user.get_user_by_uid(db, uid=decode_token(id_token))
    if not user:
        raise HTTPException(
            status_code=400, detail="No user exists",
        )
    return user


async def check_symbol(symbol: str, db: Session = Depends(get_db)):

    if not crud.stock.get_stock_by_symbol(db, symbol):
        raise HTTPException(status_code=400, detail="No such symbol exists")

    return symbol
