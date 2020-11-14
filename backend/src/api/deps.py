from typing import Generator

from fastapi import Depends, Header, HTTPException
from firebase_admin import auth
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import models
from src.db.session import SessionLocal
from src.core.utilities import HTTP400


def get_db() -> Generator:
    """Returns an instance of a Session to interact with database, and cleans up afterwards

    Yields:
        Generator: containing session instance
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def decode_token(id_token: str):
    """Decodes a firebase token to verify a user

    Args:
        id_token (str): Firebase user token

    Raises:
        HTTPException: 401 unauthenticated

    Returns:
        str: user ID
    """
    try:
        return auth.verify_id_token(id_token)["uid"]
    except Exception as e:
        raise HTTPException(401, detail="The authentication token is invalid.")


def check_user_exists(uid: str, db: Session = Depends(get_db)) -> None:
    """Checks that a user ID exists in the database

    Args:
        uid (str): user ID
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 user already exists
    """
    user = crud.user.get_user_by_uid(db=db, uid=uid)
    if user:
        raise HTTP400("User already exists.")


def get_current_user_m(id_token: str = Header(None), db: Session = Depends(get_db)) -> models.User:
    """Returns the User Model for the current user

    Args:
        id_token (str, optional): user id token. Defaults to Header(None).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: User does not exist

    Returns:
        models.User: user model
    """
    user_m = crud.user.get_user_by_uid(db=db, uid=decode_token(id_token))
    if not user_m:
        raise HTTP400("No user exists.")

    return user_m


def get_current_user_dm(
    user_m: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)
) -> "dm.UserDM":
    """Returns the User domain model for the current user

    Returns:
        domain_models.UserDM: domain model of user
    """
    return dm.UserDM(user_m, db)


async def check_symbol(symbol: str, db: Session = Depends(get_db)):
    """Checks whether a stock symbol exists in the database

    Args:
        symbol (str): stock symbol
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 Symbol doesn't exist

    Returns:
        str: stock symbol
    """
    if not crud.stock.get_by_symbol(db=db, symbol=symbol):
        raise HTTP400("No such symbol exists.")

    return symbol


def check_uid_email(email: str, uid: str):
    """Verify that user id matches email address

    Args:
        email (str): email address of user
        uid (str): user ID

    Raises:
        HTTPException: 400 user ID does not match provided email
    """
    if not auth.get_user(uid).email == email:
        raise HTTP400("The uid does not match with the provided email.")
