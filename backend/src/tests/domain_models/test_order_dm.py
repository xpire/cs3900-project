from unittest import mock

import pytest
from src import crud
from src.domain_models.order_dm import ExecutionFailedException, LimitOrder, Order
from src.game.feature_unlocker.feature_unlocker import feature_unlocker
from src.schemas.response import ResultException, Success
from src.tests.utils.common import get_mock_user, get_test_order, mock_return


@pytest.fixture
def mock_feature_unlocker(monkeypatch):
    """mocks feature_unlocker"""

    def mock_level_required(*args, **kwargs):
        return 3  # Always require level 3

    monkeypatch.setattr(feature_unlocker, "level_required", mock_level_required)


def test_order_check_submit():
    Order.__abstractmethods__ = set()

    order = get_test_order(Order, symbol="symbol", qty=10, user=get_mock_user(), db=None, trade_type="trade_type")

    order.qty = -1
    with pytest.raises(ResultException):  # Should fail
        order.check_submit().ok()


def test_order_submit(monkeypatch, mocker):

    Order.__abstractmethods__ = set()

    order = get_test_order(Order, symbol="symbol", qty=10, user=get_mock_user(), db=None, trade_type="trade_type")

    monkeypatch.setattr(order, "try_execute", mock_return(True))
    assert order.submit().success

    monkeypatch.setattr(order, "try_execute", mock_return(False))
    mock_create_order = mocker.patch("src.crud.pending_order.create_order")
    with mock.patch("src.domain_models.order_dm.Order.schema"):  # Mock out .schema() function
        assert order.submit().success
        mock_create_order.assert_called()  # Assert crud function is called


def test_order_try_execute(monkeypatch):

    Order.__abstractmethods__ = set()

    order = get_test_order(Order, symbol="symbol", qty=10, user=get_mock_user(), db=None, trade_type="trade_type")
    monkeypatch.setattr(order, "is_trading", mock_return(False))
    with pytest.raises(ResultException):  # Should fail
        order.try_execute().ok()

    monkeypatch.setattr(order, "is_trading", mock_return(True))
    with mock.patch(
        "src.domain_models.order_dm.Order._try_execute"
    ) as mock__try_execute:  # Mock out .schema() function
        order.try_execute()
        mock__try_execute.assert_called()  # Assert function is called


@mock.patch("src.domain_models.trade_dm.Trade.new")
def test_order_execute(test_new):

    Order.__abstractmethods__ = set()

    order = get_test_order(Order, symbol="symbol", qty=10, user=get_mock_user(), db=None, trade_type="trade_type")

    mock_trade = mock.MagicMock()
    test_new.return_value = mock_trade

    order.execute(0)
    mock_trade.execute.assert_called()  # Asser that this function is called

    mock_trade.execute.return_value = mock.Mock(success=False)
    with pytest.raises(ExecutionFailedException):
        order.execute(0)

    mock_trade.execute.return_value = mock.Mock(success=True)
    assert order.execute(0).success


def test_limitorder_check_submit(mock_feature_unlocker):
    order = get_test_order(
        LimitOrder, limit_price=0, symbol="symbol", qty=10, user=get_mock_user(), db=None, trade_type="trade_type"
    )
    order.user.level = 2  # Set user to level 2

    with pytest.raises(ResultException):  # Should fail
        order.check_submit().ok()

    order.user.level = 3
    order.qty = -1
    with pytest.raises(ResultException):  # Should fail
        order.check_submit().ok()

    order.qty = 1
    order.limit_price = -1
    with pytest.raises(ResultException):  # Should fail
        order.check_submit().ok()
