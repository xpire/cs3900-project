from unittest import mock

import pytest
from src.domain_models import trade_dm
from src.domain_models.trade_dm import BuyTrade, CoverTrade, SellTrade, ShortTrade, Trade
from src.schemas.transaction import OrderType, TradeType
from src.tests.utils.common import get_test_order


def mock_apply_commission(price, type):
    return price


def test_trade_execute():
    user = mock.MagicMock()

    Trade.__abstractmethods__ = set()
    trade = get_test_order(Trade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user)

    with mock.patch("src.domain_models.trade_dm.apply_commission", side_effect=mock_apply_commission):
        with mock.patch.object(trade, "check") as mock_check:
            with mock.patch.object(trade, "apply_trade") as mock_apply_trade:
                with mock.patch.object(trade, "dispatch_events") as mock_dispatch_events:
                    trade.__class__.trade_type = TradeType.BUY

                    trade.execute()
                    mock_check.assert_called_with(200, 200)
                    mock_apply_trade.assert_called_with(200, trade.transaction_schema)
                    user.add_exp.assert_called_with(0)
                    mock_dispatch_events.assert_called()


def test_trade_apply_trade():
    user = mock.MagicMock()

    Trade.__abstractmethods__ = set()
    trade = get_test_order(Trade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user)

    with mock.patch("src.crud.user.update_transaction") as mock_update_transaction:
        with mock.patch("src.crud.user.add_history") as mock_add_history:
            user.balance = 0

            trade.__class__.trade_type = TradeType.BUY
            trade.apply_trade(10, trade.transaction_schema)
            assert user.balance == -10

            user.balance = 0
            trade.__class__.trade_type = TradeType.SELL
            trade.apply_trade(10, trade.transaction_schema)
            assert user.balance == 10


def test_buytrade_check():

    user = mock.MagicMock()
    trade = get_test_order(BuyTrade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user)

    user.model.balance = 0
    assert not trade.check(1, 1).success

    user.model.balance = 1
    assert trade.check(1, 1).success


def test_selltrade_check():

    user = mock.MagicMock()
    trade = get_test_order(
        SellTrade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user
    )

    with mock.patch("src.domain_models.trade_dm.check_owned_longs") as mock_check_owned_longs:
        mock_check_owned_longs.return_value = False
        assert not trade.check(0, 0).success

        mock_check_owned_longs.return_value = True
        assert trade.check(0, 0).success


def test_shorttrade_check():
    user = mock.MagicMock()
    trade = get_test_order(
        ShortTrade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user
    )

    user.level = 1
    assert not trade.check(0, 0).success

    with mock.patch("src.domain_models.trade_dm.check_short_balance") as mock_check_short_balance:

        # Insufficient balance, fails
        mock_check_short_balance.return_value = False
        user.level = 5
        assert not trade.check(0, 0).success

        user.level = 10
        assert not trade.check(0, 0).success

        mock_check_short_balance.return_value = True
        user.level = 5
        assert trade.check(0, 0).success

        user.level = 10
        assert trade.check(0, 0).success


def test_covertrade_check():
    user = mock.MagicMock()
    trade = get_test_order(
        CoverTrade, symbol="symbol", qty=10, price=20, order_type=OrderType.MARKET, db=None, user=user
    )

    user.model.balance = 1
    user.level = 1
    assert not trade.check(0, 0).success

    user.level = 5
    with mock.patch("src.domain_models.trade_dm.check_owned_shorts") as mock_check_owned_shorts:
        mock_check_owned_shorts.return_value = False
        assert not trade.check(0, 0).success

        mock_check_owned_shorts.return_value = True
        assert not trade.check(2, 2).success
        assert trade.check(1, 1).success


def test_apply_commission():

    with mock.patch("src.domain_models.trade_dm.settings") as mock_settings:
        mock_settings.COMMISSION_RATE = 0.5

        assert trade_dm.apply_commission(price=100, is_buying=True) == 150
        assert trade_dm.apply_commission(price=100, is_buying=False) == 50

        mock_settings.COMMISSION_RATE = 0
        assert trade_dm.apply_commission(price=100, is_buying=True) == 100
        assert trade_dm.apply_commission(price=100, is_buying=False) == 100


def test_check_owned():

    with mock.patch("src.domain_models.trade_dm.find") as mock_find:
        position = mock.MagicMock()
        mock_find.return_value = None

        assert not trade_dm.check_owned(qty=10, symbol=None, positions=None)

        mock_find.return_value = position
        position.qty = 10
        assert not trade_dm.check_owned(qty=11, symbol=None, positions=None)
        assert trade_dm.check_owned(qty=10, symbol=None, positions=None)
