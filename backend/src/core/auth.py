import firebase_admin
from fastapi import HTTPException
from firebase_admin import auth, credentials

cred = credentials.Certificate("src/core/ecksdee-firebase.json")
firebase_admin.initialize_app(cred)


def decode_token(id_token: str):

    uid = None
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
    except:
        raise HTTPException(401, detail="The authentication token is invalid.")

    return uid
