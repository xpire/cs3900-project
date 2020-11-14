import datetime as dt
from unittest import mock

import pytest
from freezegun import freeze_time
from src import crud
from src.domain_models.order_dm import ExecutionFailedException, LimitOrder, MarketOrder, Order
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


@mock.patch("src.domain_models.order_dm.Order.get_curr_price")
def test_limitorder__try_execute(mock_get_curr_price):

    limit_price = 0
    order = get_test_order(
        LimitOrder,
        limit_price=limit_price,
        symbol="symbol",
        qty=10,
        user=get_mock_user(),
        db=None,
        trade_type="trade_type",
    )
    mock_get_curr_price.return_value = 10

    with mock.patch.object(order, "can_execute") as mock_can_execute:
        mock_can_execute.return_value = False
        with pytest.raises(ResultException):  # Should fail
            order._try_execute().ok()

        mock_can_execute.return_value = True
        with mock.patch.object(order, "execute") as mock_execute:
            assert order._try_execute().success
            mock_execute.assert_called_with(limit_price)


def test_limitorder_can_execute():

    limit_price = 10
    trade_type = mock.MagicMock()
    order = get_test_order(
        LimitOrder,
        limit_price=limit_price,
        symbol="symbol",
        qty=10,
        user=get_mock_user(),
        db=None,
        trade_type=trade_type,
    )

    trade_type.is_buying = True
    assert order.can_execute(9)
    assert not order.can_execute(11)

    trade_type.is_buying = False
    assert not order.can_execute(9)
    assert order.can_execute(11)


def test_marketorder__try_execute():
    order = get_test_order(
        MarketOrder,
        symbol="symbol",
        qty=10,
        user=get_mock_user(),
        db=None,
        trade_type="trade_type",
    )

    order.is_pending = True
    with mock.patch.object(order, "try_execute_pending") as mock_try_execute_pending:
        assert order._try_execute().success
        mock_try_execute_pending.assert_called()

    order.is_pending = False
    with mock.patch.object(order, "execute") as mock_execute:
        with mock.patch.object(order, "get_curr_price") as mock_get_curr_price:
            mock_get_curr_price.return_value = 10

            assert order._try_execute().success
            mock_execute.assert_called_with(10)


@freeze_time("2012-01-14 12:00:00")
@mock.patch("src.domain_models.order_dm.find")
@mock.patch("src.crud.exchange.get_exchange_by_name")
@mock.patch("src.domain_models.trading_hours.next_open")
def test_marketorder_try_executing_pending(mock_next_open, mock_get_exchange_by_name, mock_find):

    order = get_test_order(
        MarketOrder,
        symbol="symbol",
        qty=10,
        user=get_mock_user(),
        db=None,
        trade_type="trade_type",
    )
    with mock.patch.object(order, "get_stock") as mock_get_stock:
        stock = mock.MagicMock()
        mock_get_stock.return_value = stock

        mock_next_open.return_value = dt.datetime.now() + dt.timedelta(seconds=1)
        assert not order.try_execute_pending().success

        mock_next_open.return_value = dt.datetime.now() - dt.timedelta(seconds=1)
        mock_find.return_value = None
        assert not order.try_execute_pending().success

        mock_find.return_value = mock.MagicMock()
        mock_find.return_value.open = "open"
        with mock.patch.object(order, "execute") as mock_execute:
            assert order.try_execute_pending().success
            mock_execute.assert_called_with("open")
