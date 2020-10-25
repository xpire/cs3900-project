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
from src.game.event.sub_events import TransactionEvent
from src.notification.notifier import Notifier, notif_hub
from src.schemas.transaction import ClosingTransaction, OpeningTransaction, OrderType, TradeType, Transaction

router = APIRouter()

STARTING_BALANCE = 10000


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
    user = crud.user.create(
        db, obj_in=schemas.UserCreate(email=email, uid=uid, username=email, balance=STARTING_BALANCE)
    )

    return dm.UserDM(user, db).schema


@router.get("/reset_portfolio")
async def reset_user_portfolio(user_dm=Depends(get_current_user_dm), db: Session = Depends(get_db)):

    # Check if it can be reset
    if not user_dm.can_reset_portfolio():
        return {
            "result": "failed, you have reset too recently.",
            "last_reset_time": user_dm.model.last_reset,
            "current_time": datetime.now(),
        }

    crud.user.update_balance(db, user_dm.model, STARTING_BALANCE)

    crud.user.reset_user_portfolio(user_dm.model, db)
    # TODO: Keep track of resets and reset timestamp

    return {"result": "reset success."}


@router.get("/balance")
async def get_user_balance(user_m: models.User = Depends(get_current_user_m)) -> float:
    """
    Return the user's balance
    """
    return user_m.balance


@router.get("/add_exp")
async def add_exp(
    amount: float,
    user=Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> schemas.User:
    """
    Give user [amount] exp
    - exposed for testing purposes
    """
    user.add_exp(amount)
    return user.schema


@router.get("/reset_level")
async def reset_level(user=Depends(get_current_user_dm), db: Session = Depends(get_db)) -> schemas.User:
    """
    Reset user's level and exp
    - exposed for testing purposes
    """
    user.exp = 0
    user.level = 1
    user.save_to_db()
    return user.schema


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

    try:
        print("VALIDATE USER")
        id_token = await receive_json(ws)

        try:
            uid = decode_token(id_token)
        except:
            print("INVALID AUTH MESSAGE RECEIVED:", id_token)
            uid = None

        user = crud.user.get_user_by_uid(db, uid=uid)

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


"""
TEST APIS
"""


@router.post("/reset")
async def market_buy(user=Depends(get_current_user_dm)) -> schemas.User:
    user.exp = 0
    user.level = 1
    user.user.unlocked_achievements = []
    user.save_to_db()
    return user.schema


@router.post("/market/buy")
async def market_buy(symbol: str, quantity: int, user=Depends(get_current_user_dm)) -> schemas.User:
    t = OpeningTransaction(
        user=user,
        order_type=OrderType.MARKET,
        trade_type=TradeType.BUY,
        symbol=symbol,
        quantity=quantity,
        brokerage_fee=10,
        trade_timestamp=datetime.now(),
    )

    from src.game.setup.setup import event_hub

    event_hub.publish(TransactionEvent(user=user, transaction=t))
    return user.schema


@router.post("/market/sell")
async def market_buy(symbol: str, quantity: int, user=Depends(get_current_user_dm)) -> schemas.User:
    t = ClosingTransaction(
        user=user,
        order_type=OrderType.MARKET,
        trade_type=TradeType.SELL,
        symbol=symbol,
        quantity=quantity,
        brokerage_fee=10,
        trade_timestamp=datetime.now(),
        profit=1000,
        profit_percentage=10,
    )

    from src.game.setup.setup import event_hub

    event_hub.publish(TransactionEvent(user=user, transaction=t))
    return user.schema


"""
class Transaction(BaseSchema):
    user: Any  # UserDM
    order_type: OrderType
    trade_type: TradeType
    symbol: str
    quantity: int
    brokerage_fee: float
    trade_timestamp: datetime
    """
