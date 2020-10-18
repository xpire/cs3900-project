from typing import Generator
from src.db.session import SessionLocal
from fastapi import HTTPException
from firebase_admin import auth


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