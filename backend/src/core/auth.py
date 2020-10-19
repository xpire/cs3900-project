# ========================================================== #
# ██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗  #
# ██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝  #
# ██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗ #
# ██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║ #
# ╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝ #
#  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝  #
# ========================================================== #
# This file is deprecated for now

import firebase_admin
from fastapi import HTTPException
from firebase_admin import auth, credentials

# TODO move to settings
cred = credentials.Certificate("src/core/ecksdee-firebase.json")
firebase_admin.initialize_app(cred)


def decode_token(id_token: str):
    try:
        return auth.verify_id_token(id_token)["uid"]
    except Exception as e:
        raise HTTPException(401, detail="The authentication token is invalid.")
