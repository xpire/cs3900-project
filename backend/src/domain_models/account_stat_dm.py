from abc import ABC, abstractmethod

from src import schemas
from src.domain_models.data_provider.setup import get_data_provider


def position_to_dict(p):
    entry = {}
    entry["symbol"] = p.symbol
    entry["name"] = p.stock.name
    entry["price"] = get_data_provider().get_curr_day_close(p.symbol)
    entry["previous_price"] = get_data_provider().get_curr_day_open(p.symbol)
    entry["owned"] = p.qty
    entry["average_paid"] = p.avg
    entry["total_paid"] = p.avg * p.qty
    entry["value"] = entry["price"] * p.qty
    entry["profit"] = entry["value"] - entry["total_paid"]
    entry["day_profit"] = (
        entry["price"] - entry["previous_price"]
    ) * p.qty  # BUG: fix, returns daily profit, but not for the portfolio
    entry["day_return"] = entry["day_profit"] / entry["total_paid"]
    entry["total_return"] = entry["profit"] / entry["total_paid"]
    return entry


class PortfolioStat(ABC):
    def __init__(self, positions):
        self.positions = positions

    @abstractmethod
    def total_closing_value(self):
        pass

    @abstractmethod
    def total_buy_value(self):
        pass

    @abstractmethod
    def total_profit(self):
        pass

    @abstractmethod
    def total_daily_profit(self):
        pass

    def total_return(self):
        return self.percentage_return(self.total_profit())

    def total_daily_return(self):
        return self.percentage_return(self.total_daily_profit())

    def total(self, stat):
        return total(self.positions, stat)

    def percentage_return(self, profit):
        return div(profit, self.total_buy_value())


class HalfPortfolioStat(PortfolioStat):
    def _opening_value_abs(self, p):
        return p.qty * p.avg

    def _closing_value_abs(self, p):
        return p.qty * curr_price(p.symbol)

    @abstractmethod
    def opening_value(self, p):
        pass

    @abstractmethod
    def closing_value(self, p):
        pass

    @abstractmethod
    def buy_value(self, p):
        pass

    @abstractmethod
    def sell_value(self, p):
        pass

    def _price_change_since_open(self, p):
        return curr_price(p.symbol) - open_price(p.symbol)

    @abstractmethod
    def daily_profit(self, p):
        pass

    def total_opening_value(self):
        return self.total(self.opening_value)

    def total_closing_value(self):
        return self.total(self.closing_value)

    def total_buy_value(self):
        return self.total(self.buy_value)

    def total_sell_value(self):
        return self.total(self.sell_value)

    def total_profit(self):
        return self.total_opening_value() + self.total_closing_value()

    def total_daily_profit(self):
        return self.total(self.daily_profit)


class LongPortfolioStat(HalfPortfolioStat):
    """
    Buy to open and sell to close
    """

    def opening_value(self, p):
        return -self._opening_value_abs(p)

    def closing_value(self, p):
        return self._closing_value_abs(p)

    def buy_value(self, p):
        return self.opening_value(p)

    def sell_value(self, p):
        return self.closing_value(p)

    def daily_profit(self, p):
        return self._price_change_since_open(p)


class ShortPortfolioStat(HalfPortfolioStat):
    """
    Sell to open and buy to close
    """

    def opening_value(self, p):
        return self._opening_value_abs(p)

    def closing_value(self, p):
        return -self._closing_value_abs(p)

    def buy_value(self, p):
        return self.closing_value(p)

    def sell_value(self, p):
        return self.opening_value(p)

    def daily_profit(self, p):
        return -self._price_change_since_open(p)


class CombinedPortfolioStat(PortfolioStat):
    def __init__(self, long, short):
        self.long = long
        self.short = short

    def total_profit(self):
        return self.long.total_profit() + self.short.total_profit()

    def total_closing_value(self):
        return self.long.total_closing_value() + self.short.total_closing_value()

    def total_buy_value(self):
        return self.long.total_buy_value() + self.short.total_buy_value()

    def total_daily_profit(self):
        return self.long.total_daily_profit() + self.short.total_daily_profit()


class AccountStat:
    def __init__(self, user):
        self.user = user
        self.long = LongPortfolioStat(self.get_positions(is_long=True))
        self.short = ShortPortfolioStat(self.get_positions(is_long=False))
        self.portfolio = CombinedPortfolioStat(self.long, self.short)

    def net_worth(self):
        return self.balance + self.portfolio.total_closing_value()

    def gross_value(self):
        return self.balance + self.long.total_closing_value()

    def short_balance(self):
        return self.gross_value() * self.short_allowance_rate - self.short.total_opening_value()

    def compile_portfolio_stats(self):
        return schemas.PortfolioStatAPIout(
            total_long_value=self.long.total_closing_value(),
            total_short_value=self.short.total_closing_value(),
            total_portfolio_value=self.portfolio.total_closing_value(),
            total_long_profit=self.long.total_profit(),
            total_short_profit=self.short.total_profit(),
            total_portfolio_profit=self.portfolio.total_profit(),
            total_long_return=self.long.total_return(),
            total_short_return=self.short.total_return(),
            total_portfolio_return=self.portfolio.total_return(),
            daily_long_profit=self.long.total_daily_profit(),
            daily_short_profit=self.short.total_daily_profit(),
            daily_portfolio_profit=self.portfolio.total_daily_profit(),
            daily_long_return=self.long.total_daily_return(),
            daily_short_return=self.short.total_daily_return(),
            daily_portfolio_return=self.portfolio.total_daily_return(),
            balance=self.balance,
            short_balance=self.short_balance(),
            total_value=self.net_worth(),
        )

    def get_positions_info(self, is_long=True):
        def to_position_schema(p):
            return schemas.PositionAPIout(**position_to_dict(p))

        return [to_position_schema(p) for p in self.get_positions(is_long)]

    def get_positions(self, is_long=True):
        return self.user.model.long_positions if is_long else self.user.model.short_positions

    @property
    def balance(self):
        return self.user.balance

    @property
    def short_allowance_rate(self):
        return self.user.short_allowance_rate


def curr_price(symbol):
    return get_data_provider().curr_price(symbol)


def open_price(symbol):
    return get_data_provider().get_curr_day_open(symbol)


def div(a, b, default=0):
    return default if b is 0 else a / b


def total(positions, stat):
    return sum((stat(p) for p in positions))
