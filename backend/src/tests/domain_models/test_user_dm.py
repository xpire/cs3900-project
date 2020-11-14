import datetime as dt
import math
import random
from datetime import timedelta
from typing import Any, Dict

import src.crud as crud
import src.models as md
import src.schemas as sch
import src.tests.utils.common as common_utils
from freezegun import freeze_time
from sqlalchemy.orm import Session
from src.core.config import settings
from src.tests.utils.utils import clean_up

test_users = common_utils.generate_k_ranodm_users(
    init=3,
    k=10,
    shuffle=True,
)


@clean_up
def test_propertie_test(db: Session):
    def basic_property_checker(dm: Any, user: Dict) -> None:
        assert user["exp"] == dm.exp
        assert user["level"] == dm.level
        assert user["balance"] == dm.balance
        assert user["uid"] == dm.uid

    common_utils.user_diff_checker(
        db=db,
        test_users=test_users,
        checker=basic_property_checker,
    )


@clean_up
def test_can_reset_portfolio(db: Session):
    def can_reset_portfolio_checker(dm: Any, user: Dict):
        s = random.randint(1, settings.RESET_WAIT_PERIOD_SECONDS)
        for ind, test_time in [
            (
                c,
                user["last_reset"]
                + dt.timedelta(seconds=settings.RESET_WAIT_PERIOD_SECONDS)
                + c * dt.timedelta(seconds=s),
            )
            for c in range(-1, 2)
        ]:
            with freeze_time(test_time):
                if ind < 0:
                    assert not dm.can_reset_portfolio()
                else:
                    assert dm.can_reset_portfolio()

    common_utils.user_diff_checker(
        db=db,
        test_users=test_users,
        checker=can_reset_portfolio_checker,
    )


@clean_up
@freeze_time(dt.datetime.now() + dt.timedelta(seconds=settings.RESET_WAIT_PERIOD_SECONDS))
def test_reset_portfolio(db: Session):
    def reset_portfolio_checker(dm: Any, user: Dict):
        res = dm.reset()
        assert res.success
        assert dm.balance == settings.STARTING_BALANCE
        assert dm.model.long_positions == []
        assert dm.model.short_positions == []
        assert dm.model.transactions == []
        assert dm.model.net_worth_history == []
        assert dm.model.resets == (user["resets"] + 1)

    common_utils.user_diff_checker(
        db=db,
        test_users=test_users,
        checker=reset_portfolio_checker,
    )
