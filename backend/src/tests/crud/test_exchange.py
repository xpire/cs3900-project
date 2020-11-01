import src.models as md
import src.tests.utils as utils
from sqlalchemy.orm import Session


def test_exchange(db: Session) -> None:
    test_user_1 = utils.user.generate_random_user(is_init=True)
    test_user_2 = utils.user.generate_random_user(is_init=False)
    test_user_3 = utils.user.generate_random_user(is_init=False)
    test_user_4 = utils.user.generate_random_user(is_init=False)
    assert True == True
