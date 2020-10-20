from json.decoder import JSONDecodeError

from fastapi import APIRouter, Depends, Header, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from src import crud
from src import domain_models as dm
from src import models, schemas
from src.api.deps import decode_token, get_current_user_dm, get_current_user_m, get_db
from src.core.async_exit import AppStatus
from src.notification import notifier

router = APIRouter()


@router.get("")
async def check_user(id_token: str = Header(None)) -> schemas.user:

    uid = decode_token(id_token)

    return uid


@router.get("/delete")
async def delete_user(
    *,
    email: str,
    db: Session = Depends(get_db),
) -> bool:
    """
    Just a helper api for testing
    """

    return crud.user.delete_user_by_email(db, email=email)


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

    # TODO @GeorgeBai:
    # - change to post again
    # - current doesn't check whether the email matches the user's uid

    uid = decode_token(id_token)
    user = crud.user.get_user_by_uid(db, uid=uid)

    if not user:
        user = crud.user.create(db, obj_in=schemas.UserCreate(email=email, uid=uid, username=email))

    # TODO @GeorgeBai
    # raise error if already created

    return dm.UserDM(user, db).schema


@router.get("/balance")
async def get_user_balance(user: models.User = Depends(get_current_user_m), db: Session = Depends(get_db)) -> float:
    return user.balance


# TODO implement get_current_user_dm
# temporarily added for the sake of testing
@router.get("/add_exp")
async def add_exp(
    amount: float,
    user_model: models.User = Depends(get_current_user_m),
    db: Session = Depends(get_db),
) -> schemas.User:
    user = dm.UserDM(user_model, db)
    user.add_exp(amount)
    return user.schema


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


@router.get("/balance")
async def get_user_balance(user_m: models.User = Depends(get_current_user_m)) -> float:
    """
    Return the user's balance
    """
    return user_m.balance


@router.get("/add_exp")
async def add_exp(
    amount: float,
    user: models.User = Depends(get_current_user_dm),
    db: Session = Depends(get_db),
) -> schemas.User:
    """
    Give user [amount] exp
    - exposed for testing purposes
    """
    user.add_exp(amount)
    return user.schema


@router.get("/reset_level")
async def reset_level(user: models.User = Depends(get_current_user_dm), db: Session = Depends(get_db)) -> schemas.User:
    """
    Reset user's level and exp
    - exposed for testing purposes
    """
    user.exp = 0
    user.level = 1
    user.save_to_db()
    return user.schema


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
            await ws.send_json(dict(is_error=False, msg="User authorised", type="auth"))
        else:
            print("NOT AUTHORISED")
            await ws.send_json(
                dict(is_error=True, msg="User not authorised", type="auth")
            )
            await ws.close()
            return

        while not AppStatus.should_exit:
            await notifier.flush(ws)

    except WebSocketDisconnect:
        print("USER DISCONNECTED")


# NOTE: fastapi provides sample code that maybe used to notify
# the same user connected using multiple clients
# @router.websocket("/notifications")
# async def websocket_endpoint(ws: WebSocket, db: Session = Depends(get_db)):
#     await ws.accept()
#     try:
#         print("VALIDATE USER")
#         id_token = await receive_json(ws)

#         try:
#             uid = decode_token(id_token)
#         except:
#             print("INVALID AUTH MESSAGE RECEIVED:", id_token)
#             uid = None

#         user = crud.user.get_user_by_uid(db, uid=uid)

#         if user:
#             print("AUTHORISED")
#             # print(schemas.UserInDB.from_orm(user))
#             await ws.send_json(dict(is_error=False, msg="User authorised", type="auth"))
#         else:
#             print("NOT AUTHORISED")
#             await ws.send_json(dict(is_error=True, msg="User not authorised", type="auth"))
#             await ws.close()
#             return

#         while True:
#             data = await receive_json(ws)
#             await ws.send_json(dict(is_error=False, msg={"message": "hi", "recieved": data}, type="notif"))

#             # await ws.send_json(json.dumps({"message": "hi", "recieved": data}))
#     except WebSocketDisconnect:
#         print("USER DISCONNECTED")
