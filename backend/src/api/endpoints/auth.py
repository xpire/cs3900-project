from datetime import datetime
from json.decoder import JSONDecodeError
from typing import List

from fastapi import APIRouter, Depends, Header, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import models, schemas
from src.api.deps import (
    check_uid_email,
    check_user_exists,
    decode_token,
    get_current_user_dm,
    get_current_user_m,
    get_db,
)
from src.core.async_exit import AppStatus
from src.domain_models import UserDM
from src.game.achievement.achievement import UserAchievement
from src.game.event.sub_events import StatUpdateEvent, TransactionEvent
from src.game.setup.setup import event_hub
from src.notification.notifier import Notifier, notif_hub
from src.schemas.response import Fail, Response, Success, return_response, return_result
from src.schemas.transaction import ClosingTransaction, OpeningTransaction, OrderType, TradeType, Transaction

router = APIRouter()


@router.get("")
async def get_user(user=Depends(get_current_user_dm)) -> schemas.User:
    return user.schema


@router.delete("")
async def delete_user(
    email: str,
    db: Session = Depends(get_db),
) -> bool:
    """
    Just a helper api for testing
    """

    return crud.user.delete_user_by_email(db, email=email)


@router.post("")
async def create_user(
    email: str,
    id_token: str = Header(None),
    db: Session = Depends(get_db),
) -> schemas.user:

    uid = decode_token(id_token)

    # Check if email matches
    check_uid_email(email, uid)

    # Check if user exists
    check_user_exists(uid, db)

    # Create if doesn't exist
    user = crud.user.create(db, obj=schemas.UserCreate(email=email, uid=uid, username=email))

    return dm.UserDM(user, db).schema


# TODO endpoint
@router.get("/reset_portfolio")
async def reset_user_portfolio(user=Depends(get_current_user_dm), db: Session = Depends(get_db)):
    return user.reset()


@router.get("/balance")
async def get_user_balance(user_m: models.User = Depends(get_current_user_m)) -> float:
    """
    Return the user's balance
    """
    return user_m.balance


@router.get("/achievements")
async def achievements(user=Depends(get_current_user_dm)) -> List[UserAchievement]:
    """
    List of achievements and whether or not they are unlocked by the user
    """
    return user.achievements


async def receive_json(ws: WebSocket):
    try:
        return await ws.receive_json()
    except JSONDecodeError:
        return None


@router.websocket("/notifs")
async def websocket_endpoint(ws: WebSocket, db: Session = Depends(get_db)):
    await ws.accept()

    notifier = None
    try:
        print("VALIDATE USER")
        id_token = await receive_json(ws)

        try:
            uid = decode_token(id_token)
        except:
            print("INVALID AUTH MESSAGE RECEIVED:", id_token)
            uid = None

        user = crud.user.get_user_by_uid(db=db, uid=uid)

        if user:
            print("AUTHORISED")
            # print(schemas.UserInDB.from_orm(user))
            await ws.send_json(dict(msg="User authorised", is_error=False, type="auth"))
        else:
            print("NOT AUTHORISED")
            await ws.send_json(dict(msg="User not authorised", is_error=True, type="auth"))
            await ws.close()
            return

        notifier = Notifier(user)
        notif_hub.subscribe(notifier)
        while not AppStatus.should_exit:
            await notifier.flush(ws)

    except WebSocketDisconnect:
        print("USER DISCONNECTED")

    finally:
        if notifier is not None:
            notif_hub.unsusbscribe(notifier)
