import src.crud as crud
import src.models as md
import src.schemas as sch
from sqlalchemy.orm import Session
from src.tests.utils.user import *

K = 5
test_users = generate_k_ranodm_users(init=True, k=K)
gkcs = generate_k_create_schemas(k=K)


def test_create_users(db: Session) -> None:
    for u in gkcs:
        crud.user.create(db=db(), obj=u)

    all_users = crud.user.get_all_users(db=db())

    for index, user in enumerate(all_users):
        assert user.uid == gkcs[index].uid
        assert user.email == gkcs[index].email
        assert user.username == gkcs[index].username


def test_get_all_users(db: Session) -> None:
    assert True
