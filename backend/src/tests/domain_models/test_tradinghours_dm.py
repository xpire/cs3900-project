import datetime as dt
from unittest import mock

import pytest
from freezegun import freeze_time
from src.core.utilities import as_delta
from src.domain_models.trading_hours import TradingHoursManager, is_weekday, next_open, next_weekday
from src.schemas.response import ResultException
from src.tests.utils.common import get_test_order

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@freeze_time("2012-01-14 12:00:00")
def test_tradinghoursmanager_is_trading():

    trading_hours = get_test_order(TradingHoursManager)
    stock = mock.MagicMock()

    with mock.patch.object(trading_hours, "get_exchange") as mock_get_exchange:
        exchange = mock.MagicMock()
        mock_get_exchange.return_value = exchange
        exchange.timezone = "utc"
        with mock.patch.object(trading_hours, "is_trading_day") as mock_is_trading_day:

            mock_is_trading_day.return_value = False

            exchange.open = as_delta((dt.datetime.now() + dt.timedelta(seconds=1)).time())
            exchange.close = as_delta((dt.datetime.now() + dt.timedelta(seconds=2)).time())
            assert not trading_hours.is_trading(stock)

            exchange.open = as_delta((dt.datetime.now()).time())
            exchange.close = as_delta((dt.datetime.now() + dt.timedelta(seconds=1)).time())
            assert not trading_hours.is_trading(stock)

            mock_is_trading_day.return_value = True

            exchange.open = as_delta((dt.datetime.now() + dt.timedelta(seconds=1)).time())
            exchange.close = as_delta((dt.datetime.now() + dt.timedelta(seconds=2)).time())
            assert not trading_hours.is_trading(stock)

            exchange.open = as_delta((dt.datetime.now()).time())
            exchange.close = as_delta((dt.datetime.now() + dt.timedelta(seconds=1)).time())
            assert trading_hours.is_trading(stock)


@freeze_time("2012-01-14 12:00:00")
def test_tradinghoursmanager_get_trading_hours_info():

    trading_hours = get_test_order(TradingHoursManager)
    stock = mock.MagicMock()

    with mock.patch.object(trading_hours, "get_exchange") as mock_get_exchange:

        exchange = mock.MagicMock()
        mock_get_exchange.return_value = exchange
        exchange.timezone = "utc"
        exchange.open = as_delta((dt.datetime.now() + dt.timedelta(seconds=1)).time())
        exchange.close = as_delta((dt.datetime.now() + dt.timedelta(seconds=2)).time())
        with mock.patch.object(trading_hours, "is_trading") as mock_is_trading:

            mock_is_trading.return_value = True

            info = trading_hours.get_trading_hours_info(stock)
            assert info.is_trading == True
            assert info.open == as_delta(dt.datetime.strptime("2012-01-14 12:00:01", DATETIME_FORMAT).time())
            assert info.close == as_delta(dt.datetime.strptime("2012-01-14 12:00:02", DATETIME_FORMAT).time())


def test_tradinghoursmanager_is_trading_day():

    trading_hours = get_test_order(TradingHoursManager)
    stock = mock.MagicMock()

    with mock.patch.object(trading_hours, "get_exchange") as mock_get_exchange:

        exchange = mock.MagicMock()
        mock_get_exchange.return_value = exchange
        exchange.simulated = False

        assert trading_hours.is_trading_day(
            stock, dt.datetime.strptime("2020-11-13 12:00:00", DATETIME_FORMAT).date()
        )  # Friday
        assert not trading_hours.is_trading_day(
            stock, dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT).date()
        )  # Saturday

        exchange.simulated = True
        assert trading_hours.is_trading_day(stock, dt.datetime.strptime("2020-11-13 12:00:00", DATETIME_FORMAT).date())
        assert trading_hours.is_trading_day(stock, dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT).date())


def test_tradinghoursmanager_get_exchange():

    trading_hours = get_test_order(TradingHoursManager)
    exchange = mock.MagicMock()

    with mock.patch("src.domain_models.trading_hours.crud.exchange.get_exchange_by_name") as mock_get_by_name:

        mock_get_by_name.return_value = None
        with pytest.raises(ResultException):
            trading_hours.get_exchange(exchange)

        expected_ret = mock.MagicMock()
        mock_get_by_name.return_value = expected_ret
        assert trading_hours.get_exchange(exchange) == expected_ret


@pytest.mark.parametrize(
    "date,expected",
    [
        (dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).date(), True),
        (dt.datetime.strptime("2020-11-12 12:00:00", DATETIME_FORMAT).date(), True),
        (dt.datetime.strptime("2020-11-13 12:00:00", DATETIME_FORMAT).date(), True),
        (dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT).date(), False),
        (dt.datetime.strptime("2020-11-15 12:00:00", DATETIME_FORMAT).date(), False),
    ],
)
def test_is_weekday(date, expected):
    assert is_weekday(date) == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (
            dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).date(),
            dt.datetime.strptime("2020-11-12 12:00:00", DATETIME_FORMAT).date(),
        ),
        (
            dt.datetime.strptime("2020-11-12 12:00:00", DATETIME_FORMAT).date(),
            dt.datetime.strptime("2020-11-13 12:00:00", DATETIME_FORMAT).date(),
        ),
        (
            dt.datetime.strptime("2020-11-13 12:00:00", DATETIME_FORMAT).date(),
            dt.datetime.strptime("2020-11-16 12:00:00", DATETIME_FORMAT).date(),
        ),
        (
            dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT).date(),
            dt.datetime.strptime("2020-11-16 12:00:00", DATETIME_FORMAT).date(),
        ),
        (
            dt.datetime.strptime("2020-11-15 12:00:00", DATETIME_FORMAT).date(),
            dt.datetime.strptime("2020-11-16 12:00:00", DATETIME_FORMAT).date(),
        ),
    ],
)
def test_next_weekday(date, expected):
    assert next_weekday(date) == expected


@pytest.mark.parametrize(
    "datetime,exchange,expected",
    [
        (
            dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=False, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:01", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-11 12:00:01", DATETIME_FORMAT),
        ),
        (
            dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=False, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-12 12:00:00", DATETIME_FORMAT),
        ),
        (
            dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=False, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-16 12:00:00", DATETIME_FORMAT),
        ),
        (
            dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=True, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:01", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-11 12:00:01", DATETIME_FORMAT),
        ),
        (
            dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=True, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-12 12:00:00", DATETIME_FORMAT),
        ),
        (
            dt.datetime.strptime("2020-11-14 12:00:00", DATETIME_FORMAT),
            mock.MagicMock(
                simulated=True, open=as_delta(dt.datetime.strptime("2020-11-11 12:00:00", DATETIME_FORMAT).time())
            ),
            dt.datetime.strptime("2020-11-15 12:00:00", DATETIME_FORMAT),
        ),
    ],
)
def test_next_open(datetime, exchange, expected):
    assert next_open(datetime, exchange) == expected
