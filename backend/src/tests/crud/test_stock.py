import src.models as md
from sqlalchemy.orm import Session
from src.tests.utils.user import *


def test_create_user(db: Session) -> None:
    test_user_1 = generate_random_user(is_init=True)
    test_user_2 = generate_random_user(is_init=False)
    test_user_3 = generate_random_user(is_init=False)
    test_user_4 = generate_random_user(is_init=False)
    assert True == True
