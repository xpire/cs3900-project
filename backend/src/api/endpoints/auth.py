from json.decoder import JSONDecodeError
from typing import List

from fastapi import Depends, Header, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.api.deps import (
    check_uid_email,
    check_user_exists,
    decode_token,
    get_current_user_dm,
    get_current_user_m,
    get_db,
)
from src.core.async_exit import AppStatus
from src.domain_models.user_dm import UserDM
from src.game.achievement.achievement import UserAchievement
from src.notification.notifier import Notifier, notif_hub
from src.schemas.response import Result, ResultAPIRouter

router = ResultAPIRouter()


@router.get("")
async def get_user(user=Depends(get_current_user_dm)) -> schemas.UserAPIout:
    """API endpoint to get users level/exp information

    Args:
        user (domain_models.UserDM, optional): User domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        schemas.UserAPIout: Contains exp_until_next_level and is_max_level
    """
    return user.schema


@router.post("")
async def create_user(
    email: str,
    username: str,
    id_token: str = Header(None),
    db: Session = Depends(get_db),
) -> schemas.user:
    """API endpoint to create a new user

    Args:
        email (str): email address
        username (str): chosen username
        id_token (str, optional): Firebase token. Defaults to Header(None).
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        schemas.user: schema containing user information
    """
    uid = decode_token(id_token)

    # Check if email matches
    check_uid_email(email, uid)

    # Check if user exists
    check_user_exists(uid, db)

    # Create if doesn't exist
    return crud.user.create(db, obj=schemas.UserCreate(email=email, uid=uid, username=username))


@router.get("/reset")
async def reset(user: UserDM = Depends(get_current_user_dm)) -> Result:
    """API endpoint to reset a users portfolio

    Args:
        user (UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        Result: success/failure of reset
    """
    return user.reset()


@router.get("/balance")
async def get_user_balance(user_m: models.User = Depends(get_current_user_m)) -> float:
    """API endpoint to return a users current balance

    Args:
        user_m (models.User, optional): user model. Defaults to Depends(get_current_user_m).

    Returns:
        float: current avaiable balance of the user
    """
    return user_m.balance


@router.get("/achievements")
async def achievements(user: UserDM = Depends(get_current_user_dm)) -> List[UserAchievement]:
    """API endpoint to get all achievements of a user

    Args:
        user (UserDM, optional): user domain model. Defaults to Depends(get_current_user_dm).

    Returns:
        List[UserAchievement]: List of all achievements available to unlock, including those already unlocked
    """
    return user.achievements


async def receive_json(ws: WebSocket):
    """Safely receives json through websocket

    Args:
        ws (WebSocket): client websocket
    """
    try:
        return await ws.receive_json()
    except JSONDecodeError:
        return None


@router.websocket("/notifs")
async def websocket_endpoint(ws: WebSocket, db: Session = Depends(get_db)):
    """Establishes a websocket conenction with the client for future notifications to be pushed

    Args:
        ws (WebSocket): client websocket
        db (Session, optional): database session. Defaults to Depends(get_db).
    """

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