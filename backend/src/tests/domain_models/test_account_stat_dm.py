from unittest import mock

import pytest
from src.domain_models.account_stat_dm import (
    AccountStat,
    CombinedPortfolioStat,
    HalfPortfolioStat,
    div,
    position_to_dict,
    total,
)


def test_position_to_dict():

    position = mock.MagicMock()

    position.symbol = "symbol"
    position.stock.name = "name"
    position.qty = 10
    position.avg = 2

    with mock.patch("src.domain_models.account_stat_dm.get_data_provider") as mock_data_provider:

        mock_provider = mock.MagicMock()
        mock_data_provider.return_value = mock_provider

        mock_provider.get_curr_day_close.return_value = 10
        mock_provider.get_curr_day_open.return_value = 5

        expected = {
            "symbol": "symbol",
            "name": "name",
            "price": 10,
            "previous_price": 5,
            "owned": 10,
            "average_paid": 2,
            "total_paid": 20,
            "value": 100,
            "profit": 80,
            "day_profit": 50,
            "day_return": 2.5,
            "total_return": 4,
        }

        assert position_to_dict(position) == expected


@pytest.mark.parametrize(
    "qty,avg,expected",
    [(10, 10, 100), (5, 2, 10), (10, 0, 0), (10, 0.5, 5)],
)
def test_halfportfoliostat__opening_value_abs(qty, avg, expected):

    HalfPortfolioStat.__abstractmethods__ = set()
    portfolio = HalfPortfolioStat(mock.MagicMock())

    position = mock.MagicMock(qty=qty, avg=avg)

    assert portfolio._opening_value_abs(position) == expected


@pytest.mark.parametrize(
    "qty,price,expected",
    [(10, 10, 100), (5, 2, 10), (10, 0, 0), (10, 0.5, 5)],
)
def test_halfportfoliostat__closing_value_abs(qty, price, expected):

    HalfPortfolioStat.__abstractmethods__ = set()
    portfolio = HalfPortfolioStat(mock.MagicMock())

    position = mock.MagicMock(qty=qty)

    with mock.patch("src.domain_models.account_stat_dm.curr_price") as mock_curr_price:

        mock_curr_price.return_value = price

        assert portfolio._closing_value_abs(position) == expected


@pytest.mark.parametrize(
    "curr,open,expected",
    [(10, 10, 0), (5, 2, 3), (10, 0, 10), (10, 0.5, 9.5)],
)
def test_halfportfoliostat__price_change_since_open(curr, open, expected):

    HalfPortfolioStat.__abstractmethods__ = set()
    portfolio = HalfPortfolioStat(mock.MagicMock())

    position = mock.MagicMock(symbol="symbol")

    with mock.patch("src.domain_models.account_stat_dm.curr_price") as mock_curr_price:
        with mock.patch("src.domain_models.account_stat_dm.open_price") as mock_open_price:

            mock_curr_price.return_value = curr
            mock_open_price.return_value = open

            assert portfolio._price_change_since_open(position) == expected


@pytest.mark.parametrize(
    "long_ret,short_ret,expected",
    [(10, 10, 20), (5, 2, 7), (10, 0, 10), (10, 0.5, 10.5)],
)
def test_combinedportfoliostat_total_profit(long_ret, short_ret, expected):

    CombinedPortfolioStat.__abstractmethods__ = set()
    long = mock.MagicMock()
    short = mock.MagicMock()
    portfolio = CombinedPortfolioStat(long, short)

    long.total_profit.return_value = long_ret
    short.total_profit.return_value = short_ret

    assert portfolio.total_profit() == expected


@pytest.mark.parametrize(
    "long_ret,short_ret,expected",
    [(10, 10, 20), (5, 2, 7), (10, 0, 10), (10, 0.5, 10.5)],
)
def test_combinedportfoliostat_total_closing_value(long_ret, short_ret, expected):

    CombinedPortfolioStat.__abstractmethods__ = set()
    long = mock.MagicMock()
    short = mock.MagicMock()
    portfolio = CombinedPortfolioStat(long, short)

    long.total_closing_value.return_value = long_ret
    short.total_closing_value.return_value = short_ret

    assert portfolio.total_closing_value() == expected


@pytest.mark.parametrize(
    "long_ret,short_ret,expected",
    [(10, 10, 20), (5, 2, 7), (10, 0, 10), (10, 0.5, 10.5)],
)
def test_combinedportfoliostat_total_buy_value(long_ret, short_ret, expected):

    CombinedPortfolioStat.__abstractmethods__ = set()
    long = mock.MagicMock()
    short = mock.MagicMock()
    portfolio = CombinedPortfolioStat(long, short)

    long.total_buy_value.return_value = long_ret
    short.total_buy_value.return_value = short_ret

    assert portfolio.total_buy_value() == expected


@pytest.mark.parametrize(
    "long_ret,short_ret,expected",
    [(10, 10, 20), (5, 2, 7), (10, 0, 10), (10, 0.5, 10.5)],
)
def test_combinedportfoliostat_total_daily_profit(long_ret, short_ret, expected):

    CombinedPortfolioStat.__abstractmethods__ = set()
    long = mock.MagicMock()
    short = mock.MagicMock()
    portfolio = CombinedPortfolioStat(long, short)

    long.total_daily_profit.return_value = long_ret
    short.total_daily_profit.return_value = short_ret

    assert portfolio.total_daily_profit() == expected


def test_accountstat_get_profit_info_for_transaction():

    user = mock.MagicMock()
    trade = mock.MagicMock()

    account = AccountStat(user)

    trade.trade_type.is_long = True
    trade.symbol = "symbol"
    trade.price = 10
    trade.qty = 5

    positions = [mock.MagicMock(symbol="symbol", avg=5)]

    user.model.long_positions = positions

    assert account.get_profit_info_for_transaction(trade) == {"profit": 25, "profit_percentage": 1}


@pytest.mark.parametrize(
    "a,b,expected",
    [(10, 10, 1), (10, 0, 0), (0, 1, 0), (10, 0.5, 20)],
)
def test_div(a, b, expected):

    assert div(a, b) == expected


def test_total():

    positions = [mock.MagicMock(value=5), mock.MagicMock(value=7)]

    def stat(position):
        return position.value

    expected = 12

    assert total(positions, stat) == expected
