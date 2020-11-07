import src.crud as crud
import src.models as md
import src.schemas as sch
import src.tests.utils.common as common_utils
from sqlalchemy.orm import Session
from src.domain_models.user_dm import UserDM
from src.tests.utils.utils import clean_up


@clean_up
def test_user_dm_create(db: Session):
    test_users = common_utils.generate_k_ranodm_users(
        init=3,
        k=10,
        shuffle=True,
    )
    md_objs = common_utils.set_db_state(db=db, model=md.User, state=test_users)
    user_dms = [UserDM(user_m=md, db=db) for md in md_objs]

    for dm, ur in zip(user_dms, test_users):
        assert ur["exp"] == dm.exp
        assert ur["level"] == dm.level
        assert ur["balance"] == dm.balance
        assert ur["uid"] == dm.uid


# import src.crud as crud
# import src.models as md
# import src.schemas as sch
# from sqlalchemy.orm import Session
# from src.tests.utils.user import *

# K = 5
# test_users = generate_k_ranodm_users(init=True, k=K)
# gkcs = generate_k_create_schemas(k=K)


# def test_create_users(db: Session) -> None:
#     for u in gkcs:
#         crud.user.create(db=db(), obj=u)

#     all_users = crud.user.get_all_users(db=db())

#     for index, user in enumerate(all_users):
#         assert user.uid == gkcs[index].uid
#         assert user.email == gkcs[index].email
#         assert user.username == gkcs[index].username


# def test_get_all_users(db: Session) -> None:
#     assert True
